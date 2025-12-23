// 🌍 Initialize Map
var map = L.map('map').setView([39.977183, 116.329867], 14);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

var marker = L.marker([39.977183, 116.329867]).addTo(map)
  .bindPopup("Vehicle Tracking Started").openPopup();

async function fetchVehicleData() {
  try {
    const response = await fetch("http://127.0.0.1:5000/api/vehicle");
    const data = await response.json();
    
    for (let i = 0; i < data.length; i++) {
      const { latitude, longitude, speed, eta, timestamp } = data[i];
      
      marker.setLatLng([latitude, longitude]);
      map.panTo([latitude, longitude]);

      // Update Info Panel
      document.getElementById("speed").textContent = speed.toFixed(2);
      document.getElementById("eta").textContent = eta.toFixed(2);
      document.getElementById("lat").textContent = latitude.toFixed(6);
      document.getElementById("lon").textContent = longitude.toFixed(6);
      document.getElementById("time").textContent = timestamp;

      // Smooth Animation Delay
      await new Promise(resolve => setTimeout(resolve, 2000));
    }
  } catch (error) {
    console.error("Error fetching vehicle data:", error);
  }
}

// Auto Refresh (every 25 seconds)
setInterval(fetchVehicleData, 25000);

// Manual Refresh Button
document.getElementById("refresh-btn").addEventListener("click", fetchVehicleData);

// Initial Fetch
fetchVehicleData();
