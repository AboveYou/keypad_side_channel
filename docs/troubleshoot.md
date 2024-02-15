# Troubleshooting

## permission denied
If you get the permission denied error while flashing add your user to the correct group. The changes will take effect after a re-login, you can create a new login prompt and skip this step with the second command. Note that you have to launch the AppImage file from this shell.

```bash
sudo usermod -aG dialout $USER
su - $USER
```

## programmer not responding
Depending on your chip you might have another bootloader when facing this error. The bootloader can be changed in the IDE.

*> Tools > Processor > ATmega328P (old bootloader)*

