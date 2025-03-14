from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__, template_folder="templates")

@app.route("/", methods=["GET", "POST"])
def index():
	if request.method == "POST":
		ssid = request.form.get("ssid")
		password = request.form.get("password")
		save_wifi_credentials(ssid, password)
		return redirect("/restart")

	return render_template("index.html")

def save_wifi_credentials(ssid, password):
	with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as f:
		f.write(f"""
		ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
		update_config=1

		network={{
			ssid="{ssid}"
			psk="{password}"
		}}
		""")

@app.route("/restart")
def restart():
	os.system("sudo systemctl restart networking")
	os.system("sudo reboot")
	return "Rebooting..."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
