#!/bin/sh

echo "Stopping ThermoPI-Cottage"
sudo systemctl stop thermoPICottage.service  

echo "Copy file over"
sudo cp /opt/ThermoPI-Furnace/thermoPICottage.service /lib/systemd/system/thermoPICottage.service

echo "Change permissions on new file"
sudo chmod 644 /lib/systemd/system/thermoPICottage.service

echo "Reload the systemd daemon"
sudo systemctl daemon-reload

echo "Enable the new service"
sudo systemctl enable thermoPICottage.service

echo "Start the new service"
sudo systemctl start thermoPICottage.service  

echo "Check that the new service is running"
# Delay to give the pi a chance to think
sleep 7

sudo systemctl status thermoPICottage.service
