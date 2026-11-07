"""ISO 20022 Financial Messaging Engine for Bangalore Banking Operations.

Provides XML and JSON generation, parsing, and validation for RBI/NPCI standard messages:
- pacs.008.001.10: Financial Institutional / Customer Credit Transfer (RTGS / NEFT / Large Value)
- pacs.002.001.12: Payment Status Report (Settlement Confirmation / Rejection)
- camt.053.001.10: Bank-to-Customer Statement (End-of-day Treasury Reconciliation)
- pain.001.001.11: Customer Credit Transfer Initiation (Corporate GCC Payroll & Vendor Batches)
"""

from __future__ import annotations

import uuid
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ISO20022MessageType(str, Enum):
    PACS_008 = "pacs.008.001.10"
    PACS_002 = "pacs.002.001.12"
    CAMT_053 = "camt.053.001.10"
    PAIN_001 = "pain.001.001.11"


class TransactionStatusCode(str, Enum):
    ACCP = "ACCP"  # Accepted Customer Profile
    ACSC = "ACSC"  # Accepted Settlement Completed
    ACSP = "ACSP"  # Accepted Settlement in Process
    RJCT = "RJCT"  # Rejected
    PDNG = "PDNG"  # Pending


class ClearingChannel(str, Enum):
    RTGS = "RTGS"
    NEFT = "NEFT"
    IMPS = "IMPS"
    UPI = "UPI"
    BOOK_TRANSFER = "BOOK_TRANSFER"


class PartyIdentification(BaseModel):
    name: str
    account_number: str
    ifsc_code: str
    city: str = "Bengaluru"
    country: str = "IN"
    lei: Optional[str] = None  # Legal Entity Identifier (20 chars)


class CreditTransferInstruction(BaseModel):
    instruction_id: str = Field(default_factory=lambda: f"INSTR-{uuid.uuid4().hex[:10].upper()}")
    end_to_end_id: str = Field(default_factory=lambda: f"E2E-{uuid.uuid4().hex[:12].upper()}")
    amount_inr: float
    currency: str = "INR"
    debtor: PartyIdentification
    creditor: PartyIdentification
    clearing_channel: ClearingChannel = ClearingChannel.RTGS
    purpose_code: str = "TREA"  # TREA (Treasury), SALA (Salary), CASH, GDDS (Goods), etc.
    remittance_info: str = "Bangalore Intra-Bank Settlement"
    execution_date: str = Field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d"))


class Pacs008Message(BaseModel):
    message_id: str = Field(default_factory=lambda: f"IN-BLR-PACS008-{uuid.uuid4().hex[:12].upper()}")
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    settlement_method: str = "CLRG"  # Clearing
    clearing_system: str = "IN-RBI-RTGS"
    total_amount_inr: float
    number_of_transactions: int
    instructions: List[CreditTransferInstruction]


class Pacs002StatusReport(BaseModel):
    message_id: str = Field(default_factory=lambda: f"IN-BLR-PACS002-{uuid.uuid4().hex[:12].upper()}")
    original_message_id: str
    original_instruction_id: str
    original_end_to_end_id: str
    status: TransactionStatusCode
    reason_code: Optional[str] = None  # e.g., AM04 (Insufficient Funds), AC01 (Incorrect Acct)
    reason_description: Optional[str] = None
    clearing_system_ref: str = Field(default_factory=lambda: f"RBI-UTR-{uuid.uuid4().hex[:16].upper()}")
    settlement_timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class StatementEntry(BaseModel):
    entry_ref: str = Field(default_factory=lambda: f"TXN-{uuid.uuid4().hex[:8].upper()}")
    amount_inr: float
    credit_debit: str  # CRDT or DBIT
    booking_date: str
    value_date: str
    counterparty_name: str
    counterparty_ifsc: str
    description: str


class Camt053Statement(BaseModel):
    statement_id: str = Field(default_factory=lambda: f"STMT-{uuid.uuid4().hex[:10].upper()}")
    account_number: str
    account_name: str
    account_ifsc: str
    currency: str = "INR"
    opening_balance_inr: float
    closing_balance_inr: float
    total_debits_inr: float
    total_credits_inr: float
    entry_count: int
    entries: List[StatementEntry]
    statement_date: str = Field(default_factory=lambda: datetime.now(timezone.utc).strftime("%Y-%m-%d"))


class BangaloreISO20022Engine:
    """Enterprise ISO 20022 message generator, parser, and RBI/NPCI validator."""

    @staticmethod
    def generate_pacs008_xml(message: Pacs008Message) -> str:
        """Serializes a pacs.008 message to canonical ISO 20022 XML format."""
        root = ET.Element("Document", xmlns="urn:iso:std:iso:20022:tech:xsd:pacs.008.001.10")
        fi_to_fi = ET.SubElement(root, "FIToFICstmrCdtTrf")

        # Group Header
        grp_hdr = ET.SubElement(fi_to_fi, "GrpHdr")
        ET.SubElement(grp_hdr, "MsgId").text = message.message_id
        ET.SubElement(grp_hdr, "CreDtTm").text = message.created_at
        ET.SubElement(grp_hdr, "NbOfTxs").text = str(message.number_of_transactions)

        ttl_amt = ET.SubElement(grp_hdr, "TtlIntrBkSttlmAmt", Ccy="INR")
        ttl_amt.text = f"{message.total_amount_inr:.2f}"

        sttlm_inf = ET.SubElement(grp_hdr, "SttlmInf")
        ET.SubElement(sttlm_inf, "SttlmMtd").text = message.settlement_method
        clr_sys = ET.SubElement(sttlm_inf, "ClrSys")
        ET.SubElement(clr_sys, "Prtry").text = message.clearing_system

        # Credit Transfer Transaction Information
        for instr in message.instructions:
            cdt_trf = ET.SubElement(fi_to_fi, "CdtTrfTxInf")

            pmt_id = ET.SubElement(cdt_trf, "PmtId")
            ET.SubElement(pmt_id, "InstrId").text = instr.instruction_id
            ET.SubElement(pmt_id, "EndToEndId").text = instr.end_to_end_id

            intr_bk_amt = ET.SubElement(cdt_trf, "IntrBkSttlmAmt", Ccy=instr.currency)
            intr_bk_amt.text = f"{instr.amount_inr:.2f}"

            ET.SubElement(cdt_trf, "IntrBkSttlmDt").text = instr.execution_date

            # Debtor Details
            dbtr = ET.SubElement(cdt_trf, "Dbtr")
            ET.SubElement(dbtr, "Nm").text = instr.debtor.name
            dbtr_acct = ET.SubElement(cdt_trf, "DbtrAcct")
            dbtr_id = ET.SubElement(dbtr_acct, "Id")
            ET.SubElement(dbtr_id, "Othr").text = instr.debtor.account_number

            dbtr_agt = ET.SubElement(cdt_trf, "DbtrAgt")
            fin_instn_id_d = ET.SubElement(dbtr_agt, "FinInstnId")
            clr_sys_mmb_d = ET.SubElement(fin_instn_id_d, "ClrSysMmbId")
            ET.SubElement(clr_sys_mmb_d, "MmbId").text = instr.debtor.ifsc_code

            # Creditor Details
            cdtr = ET.SubElement(cdt_trf, "Cdtr")
            ET.SubElement(cdtr, "Nm").text = instr.creditor.name
            cdtr_acct = ET.SubElement(cdt_trf, "CdtrAcct")
            cdtr_id = ET.SubElement(cdtr_acct, "Id")
            ET.SubElement(cdtr_id, "Othr").text = instr.creditor.account_number

            cdtr_agt = ET.SubElement(cdt_trf, "CdtrAgt")
            fin_instn_id_c = ET.SubElement(cdtr_agt, "FinInstnId")
            clr_sys_mmb_c = ET.SubElement(fin_instn_id_c, "ClrSysMmbId")
            ET.SubElement(clr_sys_mmb_c, "MmbId").text = instr.creditor.ifsc_code

            # Remittance & Purpose
            purp = ET.SubElement(cdt_trf, "Purp")
            ET.SubElement(purp, "Cd").text = instr.purpose_code

            rmt_inf = ET.SubElement(cdt_trf, "RmtInf")
            ET.SubElement(rmt_inf, "Ustrd").text = instr.remittance_info

        return ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")

    @staticmethod
    def generate_pacs002_xml(report: Pacs002StatusReport) -> str:
        """Serializes a pacs.002 Payment Status Report to canonical XML."""
        root = ET.Element("Document", xmlns="urn:iso:std:iso:20022:tech:xsd:pacs.002.001.12")
        rpt_node = ET.SubElement(root, "FIToFIPmtStsRpt")

        grp_hdr = ET.SubElement(rpt_node, "GrpHdr")
        ET.SubElement(grp_hdr, "MsgId").text = report.message_id
        ET.SubElement(grp_hdr, "CreDtTm").text = report.settlement_timestamp

        tx_inf = ET.SubElement(rpt_node, "TxInfAndSts")
        ET.SubElement(tx_inf, "OrgnlGrpInf").text = report.original_message_id
        ET.SubElement(tx_inf, "OrgnlInstrId").text = report.original_instruction_id
        ET.SubElement(tx_inf, "OrgnlEndToEndId").text = report.original_end_to_end_id
        ET.SubElement(tx_inf, "TxSts").text = report.status.value
        ET.SubElement(tx_inf, "ClrSysRef").text = report.clearing_system_ref

        if report.reason_code:
            sts_rsn = ET.SubElement(tx_inf, "StsRsnInf")
            rsn = ET.SubElement(sts_rsn, "Rsn")
            ET.SubElement(rsn, "Cd").text = report.reason_code
            if report.reason_description:
                ET.SubElement(sts_rsn, "AddtlInf").text = report.reason_description

        return ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")

    @staticmethod
    def generate_camt053_statement(statement: Camt053Statement) -> str:
        """Generates Bank-to-Customer statement XML for reconciliation."""
        root = ET.Element("Document", xmlns="urn:iso:std:iso:20022:tech:xsd:camt.053.001.10")
        stmt_root = ET.SubElement(root, "BkToCstmrStmt")

        grp_hdr = ET.SubElement(stmt_root, "GrpHdr")
        ET.SubElement(grp_hdr, "MsgId").text = f"CAMT-{statement.statement_id}"
        ET.SubElement(grp_hdr, "CreDtTm").text = datetime.now(timezone.utc).isoformat()

        stmt_node = ET.SubElement(stmt_root, "Stmt")
        ET.SubElement(stmt_node, "Id").text = statement.statement_id
        ET.SubElement(stmt_node, "CreDtTm").text = statement.statement_date

        acct = ET.SubElement(stmt_node, "Acct")
        ET.SubElement(acct, "Id").text = statement.account_number
        ET.SubElement(acct, "Nm").text = statement.account_name
        ET.SubElement(acct, "Ccy").text = statement.currency

        # Opening Balance
        op_bal = ET.SubElement(stmt_node, "Bal")
        ET.SubElement(op_bal, "Tp").text = "OPBD"
        ET.SubElement(op_bal, "Amt", Ccy=statement.currency).text = f"{statement.opening_balance_inr:.2f}"
        ET.SubElement(op_bal, "CdtDbtInd").text = "CRDT"

        # Entries
        for entry in statement.entries:
            ntry = ET.SubElement(stmt_node, "Ntry")
            ET.SubElement(ntry, "NtryRef").text = entry.entry_ref
            ET.SubElement(ntry, "Amt", Ccy=statement.currency).text = f"{entry.amount_inr:.2f}"
            ET.SubElement(ntry, "CdtDbtInd").text = entry.credit_debit
            ET.SubElement(ntry, "Sts").text = "BOOK"
            ET.SubElement(ntry, "BookgDt").text = entry.booking_date
            ET.SubElement(ntry, "ValDt").text = entry.value_date

            tx_dtls = ET.SubElement(ntry, "NtryDtls")
            ET.SubElement(tx_dtls, "CtryPtyNm").text = entry.counterparty_name
            ET.SubElement(tx_dtls, "CtryPtyIFSC").text = entry.counterparty_ifsc
            ET.SubElement(tx_dtls, "Ustrd").text = entry.description

        # Closing Balance
        cl_bal = ET.SubElement(stmt_node, "Bal")
        ET.SubElement(cl_bal, "Tp").text = "CLBD"
        ET.SubElement(cl_bal, "Amt", Ccy=statement.currency).text = f"{statement.closing_balance_inr:.2f}"
        ET.SubElement(cl_bal, "CdtDbtInd").text = "CRDT"

        return ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")

    @staticmethod
    def parse_iso20022_xml(xml_content: str) -> Dict[str, Any]:
        """Parses any incoming ISO 20022 XML document and extracts header and payload."""
        root = ET.fromstring(xml_content)
        tag = root.tag
        # strip namespace
        if "}" in tag:
            tag = tag.split("}", 1)[1]

        parsed: Dict[str, Any] = {
            "root_element": tag,
            "namespace": root.tag.split("}")[0].strip("{") if "}" in root.tag else "",
            "elements": {},
        }

        # Recursively summarize elements
        for child in root.iter():
            clean_tag = child.tag.split("}", 1)[1] if "}" in child.tag else child.tag
            if child.text and child.text.strip():
                parsed["elements"][clean_tag] = child.text.strip()

        return parsed

    @staticmethod
    def validate_ifsc_code(ifsc: str) -> bool:
        """Validates standard Indian Financial System Code (11 alphanumeric characters, 5th char is 0)."""
        if len(ifsc) != 11:
            return False
        if not ifsc[:4].isalpha() or not ifsc[:4].isupper():
            return False
        if ifsc[4] != "0":
            return False
        if not ifsc[5:].isalnum():
            return False
        return True

    @staticmethod
    def create_sample_pacs008(
        amount_inr: float = 25000000.0,  # 2.5 Crore INR
        debtor_bank: str = "Canara Bank Bangalore Head Office",
        debtor_ifsc: str = "CNRB0000001",
        debtor_account: str = "0001101009876",
        creditor_bank: str = "Goldman Sachs Services India Pvt Ltd",
        creditor_ifsc: str = "HDFC0000001",
        creditor_account: str = "50200012345678",
        purpose: str = "TREA",
        remittance_note: str = "Inter-bank Collateral Margin Settlement Bangalore",
    ) -> Pacs008Message:
        """Helper to create a validated sample pacs.008 credit transfer message."""
        instr = CreditTransferInstruction(
            amount_inr=amount_inr,
            debtor=PartyIdentification(
                name=debtor_bank,
                account_number=debtor_account,
                ifsc_code=debtor_ifsc,
                city="Bengaluru",
            ),
            creditor=PartyIdentification(
                name=creditor_bank,
                account_number=creditor_account,
                ifsc_code=creditor_ifsc,
                city="Bengaluru",
            ),
            clearing_channel=ClearingChannel.RTGS,
            purpose_code=purpose,
            remittance_info=remittance_note,
        )
        return Pacs008Message(
            total_amount_inr=amount_inr,
            number_of_transactions=1,
            instructions=[instr],
        )
