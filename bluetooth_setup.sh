if [ -z "$*" ]; then echo "Please pass in the mac address of the NXT to add"; fi

PIN="1234"

echo "$1 $PIN" | sudo tee -a /var/lib/bluetooth/$(sudo ls /var/lib/bluetooth/)/pincodes
echo "$1 added to the bluetooth file"