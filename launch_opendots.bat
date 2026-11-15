@echo off
title OpenDots AI Coworkers - Omniverse
echo ========================================================
echo   Launching OpenDots AI Coworker Workspace
echo ========================================================
cd /d "%~dp0OpenDots"
node --env-file-if-exists=.env dist/server/server/index.js
pause
