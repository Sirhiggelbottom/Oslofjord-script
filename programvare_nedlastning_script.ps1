$verChck = $PSVersionTable.PSVersion.Major -lt 7

if($verChck){
    Write-Host "Current Powershell version ("$PSVersionTable.PSVersion") is too old, installing the newest version..."
    $choice = Read-Host "Restart is required, you can restart now, or close powershell or simply exit the script. Y-Y, Y-N, N"

    Invoke-Expression "& { $(Invoke-RestMethod https://aka.ms/install-powershell.ps1) } -UseMSI"

    if ($choice -eq "Y-Y"){
        Write-Host "Restarting PC in 10 seconds"
        Start-Sleep -Seconds 10
        Restart-Computer
    } elseif ($choice -eq "Y-N"){
        Write-Host "Closing Powershell"
        Stop-Process -Id $PID
    } elseif ($choice -eq "N") {
        Write-Host "Exiting the script"
        exit 0
    } else {
        Write-Error "Wrong parameter used. Use Y-Y to restart, Y-N to close Powershell, N to exit the scipt"
        exit 1
    }
    
}

$username = Read-Host "Enter username"

$userProfilePath = "C:\Users\$username"

if (-Not (Test-Path $userProfilePath)){
    Write-Host "User profile for '$username' doesn't exist" -ForegroundColor Red
    exit
}

$downloadFolder = Join-Path $userProfilePath "Downloads"

$downloads = @{
    "UCS.zip" = "https://www.gavazziautomation.com/fileadmin/images/PIM/OTHERSTUFF/ucs.zip";
    "UWP.zip" = "http://gavazziautomation.com/images/PIM/OTHERSTUFF/uwp3.0_tool_8.5.37.3.zip";
    "VSCodeUserSetup-x64.exe" = "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user";
    "Angry IP Scanner_setup.exe" = "https://github.com/angryip/ipscan/releases/download/3.9.1/ipscan-3.9.1-setup.exe";
    "Wireshark_setup-x64.exe" = "https://2.na.dl.wireshark.org/win64/Wireshark-4.4.6-x64.exe";
    "Modbus Poll_setup-x64.exe" = "https://www.modbustools.com/download/ModbusPollSetup64Bit.exe";
    "LLDP_setup.exe" = "https://r.hanewin.net/lldp1431.exe";
    "Github desktop_setup.exe" = "https://central.github.com/deployments/desktop/desktop/latest/win32";
    "Git bash_setup.exe" = "https://github.com/git-for-windows/git/releases/download/v2.49.0.windows.1/Git-2.49.0-64-bit.exe"
}

foreach($fileName in $downloads.Keys){
    $url = $downloads[$fileName]

    $destinationPath = Join-Path -Path $downloadFolder -ChildPath $fileName

    if(Test-Path $destinationPath){
        Write-Host ""$fileName" already exists`n"
    } else {
        Write-Host "Downloading $fileName..."

        try {
            Invoke-WebRequest -Uri $url -OutFile $destinationPath
            Write-Host "$fileName Downloaded.`n"
        }
        catch {
            Write-Host "Error, Couldn't download "$fileName" because: $($_.Exception.Message)" -ForegroundColor Red
        }
        
    }
}

Write-Host "Finished"