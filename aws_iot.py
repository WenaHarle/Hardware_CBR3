# aws_iot.py

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from tempfile import NamedTemporaryFile
import os

class AWSIoTClient:
    def __init__(self):
        # AWS IoT Core endpoint
        self.host = "a1i6me6914qtwx-ats.iot.ap-southeast-1.amazonaws.com"

        # Root CA certificate text
        self.root_ca_cert = """
        -----BEGIN CERTIFICATE-----
        MIIDQTCCAimgAwIBAgITBmyfz5m/jAo54vB4ikPmljZbyjANBgkqhkiG9w0BAQsF
        ADA5MQswCQYDVQQGEwJVUzEPMA0GA1UEChMGQW1hem9uMRkwFwYDVQQDExBBbWF6
        b24gUm9vdCBDQSAxMB4XDTE1MDUyNjAwMDAwMFoXDTM4MDExNzAwMDAwMFowOTEL
        MAkGA1UEBhMCVVMxDzANBgNVBAoTBkFtYXpvbjEZMBcGA1UEAxMQQW1hem9uIFJv
        b3QgQ0EgMTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALJ4gHHKeNXj
        ca9HgFB0fW7Y14h29Jlo91ghYPl0hAEvrAIthtOgQ3pOsqTQNroBvo3bSMgHFzZM
        9O6II8c+6zf1tRn4SWiw3te5djgdYZ6k/oI2peVKVuRF4fn9tBb6dNqcmzU5L/qw
        IFAGbHrQgLKm+a/sRxmPUDgH3KKHOVj4utWp+UhnMJbulHheb4mjUcAwhmahRWa6
        VOujw5H5SNz/0egwLX0tdHA114gk957EWW67c4cX8jJGKLhD+rcdqsq08p8kDi1L
        93FcXmn/6pUCyziKrlA4b9v7LWIbxcceVOF34GfID5yHI9Y/QCB/IIDEgEw+OyQm
        jgSubJrIqg0CAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8EBAMC
        AYYwHQYDVR0OBBYEFIQYzIU07LwMlJQuCFmcx7IQTgoIMA0GCSqGSIb3DQEBCwUA
        A4IBAQCY8jdaQZChGsV2USggNiMOruYou6r4lK5IpDB/G/wkjUu0yKGX9rbxenDI
        U5PMCCjjmCXPI6T53iHTfIUJrU6adTrCC2qJeHZERxhlbI1Bjjt/msv0tadQ1wUs
        N+gDS63pYaACbvXy8MWy7Vu33PqUXHeeE6V/Uq2V8viTO96LXFvKWlJbYK8U90vv
        o/ufQJVtMVT8QtPHRh8jrdkPSHCa2XV4cdFyQzR1bldZwgJcJmApzyMZFo6IQ6XU
        5MsI+yMRQ+hDKXJioaldXgjUkK642M4UwtBV8ob2xJNDd2ZhwLnoQdeXeGADbkpy
        rqXRfboQnoZsG4q5WTP468SQvvG5
        -----END CERTIFICATE-----
        """

        # Thing certificate
        self.thing_cert = """
        -----BEGIN CERTIFICATE-----
        MIIDWjCCAkKgAwIBAgIVANf0yEwccVh47j/hd7i7oAh7B1cCMA0GCSqGSIb3DQEB
        CwUAME0xSzBJBgNVBAsMQkFtYXpvbiBXZWIgU2VydmljZXMgTz1BbWF6b24uY29t
        IEluYy4gTD1TZWF0dGxlIFNUPVdhc2hpbmd0b24gQz1VUzAeFw0yNDAyMTcwMDMz
        NTVaFw00OTEyMzEyMzU5NTlaMB4xHDAaBgNVBAMME0FXUyBJb1QgQ2VydGlmaWNh
        dGUwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCkZhjWDdlVHrHrFUdX
        NPONy+881PFKbweRwSeIlxyBsO4Vb/lSUfYL73OOkfhgKePTdhbuNZCKap9TdYjL
        A6y/g/NuY1D6vhoQ8S/iGRtfyAHc+aPJrSTJfsiGnMto4rDk7MMJN8cNlvO09KC/
        wAcic32RHTWQ6aU4rEA3yK0fj9GNILPcqW9S/iwDaGfnTyCwjD3SnkgJAAyT9pUY
        MeqOT3687+nGSpsgKuSbpREBMSyTtaVyuS0G9P7gTUNbwYIoqai88ZUdBinYyVkH
        qhDF5UDGw/qBRN3TZf8wHfz7+w9llm5ocO9RSEw8shlSdy3TckqS3b0jR6eMY17D
        u9mvAgMBAAGjYDBeMB8GA1UdIwQYMBaAFBWhgwxlO5ZAmvx5ETaw4+SsqyAQMB0G
        A1UdDgQWBBQ0viEEIoyTBvnUY1Ev3wLNTeYHyzAMBgNVHRMBAf8EAjAAMA4GA1Ud
        DwEB/wQEAwIHgDANBgkqhkiG9w0BAQsFAAOCAQEAE3Uerrrp13qXi2L/c6Tx/TW4
        TLU9W5EUQWmSvS2xb7Dso7F3l5hCc8+rd+s4oN8kzzHWbdYAzWLBcFQPyi6tYC+w
        5atFtKcoWt0tTTLHxgUBbh9QQ6Wj2D3kBwX98VSx72ovtP54cER1X4EvL4FvMxHB
        4kgQyoopOxBg1rrXUOG3ah5PQNOg89KwxNKjVipFQxwxrYyCWpUITeaYNDbKeM7r
        P/Y782O5ztB7+iDO7zX1uZwyMBzFbFjo+2h/etbb+V/d17Et2QkNisxLDvRcoHKj
        hXW4JqCx07dFhRLBcWR2MQ3NPUyaT4bOoKuM87qRtnYNj5IANb6WJRMDxQNQew==
        -----END CERTIFICATE-----
        """

        # Private key text
        self.private_key = """
        -----BEGIN RSA PRIVATE KEY-----
        MIIEpQIBAAKCAQEApGYY1g3ZVR6x6xVHVzTzjcvvPNTxSm8HkcEniJccgbDuFW/5
        UlH2C+9zjpH4YCnj03YW7jWQimqfU3WIywOsv4PzbmNQ+r4aEPEv4hkbX8gB3Pmj
        ya0kyX7IhpzLaOKw5OzDCTfHDZbztPSgv8AHInN9kR01kOmlOKxAN8itH4/RjSCz
        3KlvUv4sA2hn508gsIw90p5ICQAMk/aVGDHqjk9+vO/pxkqbICrkm6URATEsk7Wl
        crktBvT+4E1DW8GCKKmovPGVHQYp2MlZB6oQxeVAxsP6gUTd02X/MB38+/sPZZZu
        aHDvUUhMPLIZUnct03JKkt29I0enjGNew7vZrwIDAQABAoIBAQChAeEHGy8j/1ju
        zLs+/Hwf/oACyua6KH14UXzfeGeR2O+EDVNYPS9FRzGcivd/budTPc99YvZ5qaz6
        9xyO/71bH+b00M4JlM9AkoZ74Gz/5Il2mwO/TBTARqwrsjpBMetfeUYWrAsGEzYB
        nqgkw/P42LU8vyesEjgfhguq1p4/TnAou5WWOk6l96H9TvKMLV+XuMYp3ggwsDE/
        OTe/BI9LFOARg6CX+hLWU6y5XZmrEd4JqrnI1muRI+V9qAOMPalX8azhP04zCSjq
        3wzA2XIiHLBxjoHfWG9EJwtlUUKEoEJs66N27q6u3gblpkYlDT6xMPH3SBC07Yxe
        +gFq5KBxAoGBANTAIZHdWojoLdOnQuEs2pQVAhnosJEe5xY+AUNn58ey72ZMnM3N
        uniD8YC1uufWWPmDurfLKftbqrpNf5NizfSlHT+dYBuTUZxmnMhw/BAnAvjSPnSk
        8VSxPHkbk2jmo+Y3geiW2D0DSDHQZx9yDXhhTHsdylz2gj8bLv27VEnXAoGBAMXR
        qwrnoQsJzRg/32CsgQCOWCMlO3xH8t1YqiL0bGVYnuOsedpTh4dgm0FQXJgJRHdQ
        o2M4bofjvryWnEX+aSeN3dgNDI6juYGi0U5cRZB7iOjA3PPTzkMxeghn9B43bkow
        GBY+M7KvdbhdH8D72BUu844V29orlurLmQnabePpAoGBAJ0QZvgn4dHXDxYFkrNo
        iMnwJIf6KHhKxzG9fvNDf3MH4AO3JcAuVK7qQd3SzHSh4zf6D1vm6kx+ZTF7S2cE
        96XYTBqN1ckl3odHnhHAj+Zg1qnZlXBJ4Ty0SD/kotQ8Cd5JNmf/DQ8mICNehvNJ
        ITaxJmRyHta4ynlKWUvLA7QrAoGAfwM7XjoQ5cR6Qiqooyq/fXrnzlEWm5qarlJC
        k0T64CuBgU95wZvGNj7qEIqnmRrCMhW9gnR2S5wIGJBfcHWEUNg+63ydZmxrLHg9
        CaInLDiVVFSYyZliIzR+VS1hyZDvqISuwoFXslAENsbcH43UVO2bhcw1KCS6trDY
        50GvMxkCgYEAsslThKz6objTnwB7xPzDuoPZ8u3e4p+muxkZyLlkO+7LfK8IQ+iX
        6xft7ykpvkqF+gnZqcGS5bcIvAAhUTVvJvaImQXN7cSqCwgKP8HMrXut4gxlM+u2
        BEth4ngPeGKnnTTDrv3ueSCmneAOufcnCq/QGVi/mE5Bggy2stJip24=
        -----END RSA PRIVATE KEY-----
        """

        self.root_ca_cert_file = NamedTemporaryFile(delete=False)
        self.root_ca_cert_file.write(self.root_ca_cert.encode('utf-8'))
        self.root_ca_cert_file.close()

        self.private_key_file = NamedTemporaryFile(delete=False)
        self.private_key_file.write(self.private_key.encode('utf-8'))
        self.private_key_file.close()

        self.thing_cert_file = NamedTemporaryFile(delete=False)
        self.thing_cert_file.write(self.thing_cert.encode('utf-8'))
        self.thing_cert_file.close()

    def connect(self):
        # Initialize MQTT Client
        self.mqtt_client = AWSIoTMQTTClient("wena")

        # Configure MQTT Client
        self.mqtt_client.configureEndpoint(self.host, 8883)
        self.mqtt_client.configureCredentials(self.root_ca_cert_file.name, self.private_key_file.name, self.thing_cert_file.name)

        # Connect to AWS IoT Core
        self.mqtt_client.connect()

    def publish(self, topic, payload):
        self.mqtt_client.publish(topic, payload, 0)

    def subscribe(self, topic, callback):
        self.mqtt_client.subscribe(topic, 1, callback)

    def cleanup(self):
        # Remove temporary files
        os.unlink(self.root_ca_cert_file.name)
        os.unlink(self.private_key_file.name)
        os.unlink(self.thing_cert_file.name)
