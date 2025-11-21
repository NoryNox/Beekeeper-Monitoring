// js/alarm.js
// Alarm-Modul – Push/SMS/E-Mail
async function sendAlarm(message, imageBase64) {
  // Push (kostenlos)
  if ('Notification' in window && Notification.permission === "granted") {
    new Notification("Beekeeper Alarm", {body: message});
  }

  // Backend-Alarm (SMS/E-Mail)
  if (CONFIG.backendUrl) {
    try {
      await fetch(`${CONFIG.backendUrl}/api/alert`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({device_id: localStorage.getItem('deviceId'), message, image: imageBase64})
      });
    } catch (e) {
      console.warn("Alarm-Versand fehlgeschlagen", e);
    }
  }
}
