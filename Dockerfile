# Use a Windows base image
FROM mcr.microsoft.com/windows/servercore:ltsc2022

# Install additional software or perform configurations
RUN powershell -Command Install-WindowsFeature Web-Server

# Set the default command to PowerShell
CMD ["powershell.exe"]
