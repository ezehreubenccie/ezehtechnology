Import-Csv C:\radius_clients\2960xSwitch_rad_clients.csv | Foreach-Object  {
    $DeviceName = $_."Device Name"  
    $IPAddress = $_."Tags"  
    $SecretePass = "xxxx"  
    set-NpsRadiusClient -Address $IPAddress -Name $DeviceName -SharedSecret $SecretePass -VendorName Cisco -AuthAttributeRequired $False  
}  

Read-Host -Prompt "Press any key to continue"
