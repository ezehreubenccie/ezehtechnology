Import-Csv C:\radius_clients\UTD_radius_clients.csv | Foreach-Object  
{  
    $DeviceName = $_."Device Name"  
    $IPAddress = $_."Tags"  
    $SecretePass = "xxxx"  
    New-NpsRadiusClient -Address $IPAddress -Name $DeviceName -SharedSecret $SecretePass -VendorName Cisco -AuthAttributeRequired $True  
}  
