

1. Instalar python 3.11
2. Instalar JDK 17
3. Instalar node js
4. Instalar appium:
    - npm install -g appium
        - appium -v
    - appium driver install uiautomator2
        - appium driver list
5. Instalar Android estudio
6. Instalar librerias de python
    pip install -r requirements.txt

comando para ejeuctar appium
appium

comando para ejecutar emulador
- emulator -list-avds
- emulator -avd Small_Phone

"C:\Users\QA No Funcional\AppData\Local\Android\Sdk\emulator\emulator.exe" -avd Pixel_3a_API_36_extension_level_17_x86_64

comando para ejecutar test
pytest tests\23_APP_Venta_por_monto_Importe_de_un_Fecha_Mismo_Dia_FMD_manual_informada_por_monto.py -v -s

pytest tests\.py -v -s

comando para confirmar el packacge del apk
adb shell pm list packages -3

comando para validar el log de la aplicacion 
adb logcat -v time > "C:\Users\JH555XR\OneDrive - EY\Desktop\logcat_full.txt"
s
Configurar Internet en el Emulador
emulator -avd Medium_Phone_API_36.1 -dns-server 8.8.8.8,8.8.4.4

