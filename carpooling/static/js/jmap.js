const searchInput = document.querySelector('.destination');
const locations = document.querySelector('.locations');
const locationItems = document.querySelectorAll('.location');
let marker, circle, zoomed, dMarker, endLon, endLat, startLat, startLon, accuracy, polyline;
let currenRroute, currentDest, current_location;
const west = 30.8203;
const south = 38.6769;
const east = 33.8558;
const north = 40.7537;
const center = [39.9334, 34.8597];

mapboxgl.accessToken = 'pk.eyJ1IjoiaG9ycGVhenkiLCJhIjoiY2xmNjFuOGJyMWk0bzN2cjBzZno0NXNmdCJ9.aEgc6K_vrA2mctaeIFzBrg';

// Create a new Mapbox map
const map = new mapboxgl.Map({
  container: 'map',
  projection: 'globe',
  pitch: 60,
  bearing: -60,
  style: 'mapbox://styles/horpeazy/clf7ms36k001c01qoerxs6zdt',
  center: center,
  zoom: 13,
  zoomControl: true
});

// Add a marker to the map
marker = new mapboxgl.Marker()
  .setLngLat([5.6258, 6.3382])
  .addTo(map);

// When the marker is clicked, show the Street View panorama
marker.getElement().addEventListener('click', function () {
  const panorama = new mapboxgl.Popup({
    closeButton: true,
    closeOnClick: false,
    anchor: 'top-left',
    offset: [0, 0]
  });

  panorama.setDOMContent(document.getElementById('panorama'));

  const panoramaOptions = {
    position: {
      lat: startLat,
      lng: startLon
    },
    pov: {
      heading: 0,
      pitch: 0
    }
  };

  // Create a new Street View panorama
  const streetView = new mapboxgl.StreetViewPanorama(panoramaOptions);

  // Add the Street View panorama to the map
  map.addControl(streetView);

  // Open the Street View panorama in the popup
  panorama.setLngLat(marker.getLngLat()).addTo(map);
});

map.addControl(new mapboxgl.NavigationControl(), 'top-left');

// Direction Form
const directions = new MapboxDirections({
        	accessToken: mapboxgl.accessToken
    	});

function direction_reset () {
    		directions.actions.clearOrigin();
    		directions.actions.clearDestination();
    		directions.container.querySelector('input').value = '';
}
$(function () {
    		$('#get-direction').click(function () {
        		// Adding Direction form and instructions on map
        		map.addControl(directions, 'top-left');
        		directions.container.setAttribute('id', 'direction-container');
        		$(geocoder.container).hide();
        		$(this).hide();
        		$('#end-direction').removeClass('d-none');
        		$('.marker').remove();
    		});
    		$('#end-direction').click(function () {
        		direction_reset();
        		$(this).addClass('d-none');
        		$('#get-direction').show();
        		$(geocoder.container).show();
        		map.removeControl(directions);
    		});
});

function drawRoute (startLat, startLon, endLat, endLon) {
  const routeUrl = 'https://api.mapbox.com/directions/v5/mapbox/driving';
  const options = 'geometries=geojson&overview=full';
  fetch(`${routeUrl}/${startLon},${startLat};${endLon},${endLat}?${options}&access_token=${mapboxgl.accessToken}`)
    .then(function (response) {
    			if (!response.ok) {
      				throw new Error(`HTTP error! status: ${response.status}`);
    			}
    			return response.json();
  		})
  		.then(function (json) {
    			// Check if the response contains a valid route object
    			if (!json.routes || json.routes.length === 0) {
      				throw new Error('No route found.');
    			}

    			// Get the first route from the response
    			const route = json.routes[0];

    			// Create a GeoJSON object from the route geometry
    			const routeGeoJSON = {
      				type: 'Feature',
      				properties: {},
      				geometry: route.geometry
    			};

    			// Add the route layer to the map
    			map.addLayer({
      				id: 'route',
      				type: 'line',
      				source: {
        				type: 'geojson',
        				data: routeGeoJSON
      				},
      				layout: {
        				'line-join': 'round',
        				'line-cap': 'round'
      				},
      				paint: {
        				'line-color': 'red',
        				'line-width': 4
      				}
    			});

    			const dMarker = new mapboxgl.Marker()
    				.setLngLat([endLon, endLat])
    				.addTo(map);

    			// Extract the coordinates of the route geometry
      // const coordinates = route.geometry.coordinates;

      // Convert the coordinates to a list of lists
      // const routeList = coordinates.map(coord => [coord[0], coord[1]]);

    			// Fit the map view to the route bounds
    			const bounds = new mapboxgl.LngLatBounds();
    			routeGeoJSON.geometry.coordinates.forEach((coord) => bounds.extend(coord));
    			map.fitBounds(bounds, { padding: 50 });

        		// Insert the find match button
        		const matchEl = document.querySelector('.match');
        			matchEl.innerHTML = '<button class="match-btn">Find Match</button>';
        			const matchBtn = document.querySelector('.match-btn');
        			matchBtn.addEventListener('click', (e) => {
        				matchBtn.innerHTML = '<div class=\'spinner\'></div>';
        				fetch(routeUrl + startLon + ',' + startLat + ';' + endLon + ',' + endLat + '?geometries=geojson')
        				.then(function (response) {
        					return response.json();
    					})
    					.then(function (json) {
        					// Parse the response and create a LatLng array for the route
        					const route = json.routes[0];
        					const lineString = route.geometry;
        					currentRoute = [];
        					for (let i = 0; i < lineString.coordinates.length; i++) {
            						currentRoute.push([lineString.coordinates[i][1], lineString.coordinates[i][0]]);
        					}
        					fetch('/match/passenger/', {
        						method: 'POST',
        						headers: {
        							'Content-Type': 'application/json'
        						},
        						body: JSON.stringify({
        							route: currentRoute,
        							destination: currentDest,
        							location: current_location,
        							origin_lat: startLat,
        							origin_lon: startLon,
        							destination_lat: endLat,
        							destination_lon: endLon
        						})
        					})
        					.then(res => {
        						if (res.status !== 200) {
        							throw new Error();
        						}
        						return res.json();
        					})
        					.then(data => {
        						const resultEl = document.querySelector('.results');
        						resultEl.innerHTML = '';
        						const id = data.id;
        						data = data.result;
        						if (data.length < 1) {
        							resultEl.innerHTML = '<div>No match found!</div>';
        							resultEl.innerHTML += `<div class="end-ride-wrapper"  style="width: 100%;
        										display: flex; justify-content: flex-end; margin-top: 50px;">
											<a href="/end-trip/${id}" class="end-ride-btn" 
											style="min-width:150px; padding: 10px; 
											background-color: red; border: none; color: white; 
											font-size: 16px; cursor: pointer; font-weight: bold; 
											border-radius: 8px; text-align: center;">End Ride</a>
											</div>`;
        							matchBtn.style.display = 'none';
        							return;
        						}

        						for (let i = 0; i < data.length; i++) {
        							resultEl.innerHTML += `<div class="match-wrapper">
											<div><span>Username: </span>${data[i].username}</div>
											<div><span>Destination:</span> ${data[i].destination} </div>
											<div><span>Origin: </span>${data[i].origin} </div>
											<div><span>Match rate:</span> ${data[i].match_rate}%</div>
											<div style="width: 100%; display: flex; justify-content: 
											flex-end; margin-top: 5px;">
											<a href="/match/passenger/?trip_id=${id}&match_id=${data[i].id}"
											style="min-width:150px; padding: 5px; background-color: green;
											border: none; color: white; font-size: 14px; cursor: pointer;
											font-weight: bold; border-radius: 4px; text-align: center;">
											Offer ride</a></div>
											</div>`;
        						}
        						matchBtn.style.display = 'none';
        						resultEl.innerHTML += `<div class="end-ride-wrapper" style="width: 100%; display: flex;
        								        justify-content: flex-end; margin-top: 50px;">
										<a href="/end-trip/${id}" class="end-ride-btn" style="min-width:150px;
										padding: 10px; background-color: red; border: none; color: white;
										font-size: 16px; cursor: pointer; font-weight: bold; border-radius: 8px;
										text-align: center;">End Ride</a>
									       </div>`;
        					})
        					.catch(error => {
        						console.log(error);
        						matchBtn.innerHTML = 'Find Match';
        					});
        				});
        			});
    			});
}

function distance (lat1, lon1, lat2, lon2) {
  lat1 = parseFloat(lat1);
  lat2 = parseFloat(lat2);
  lon1 = parseFloat(lon1);
  lon2 = parseFloat(lon2);
  		const R = 6371; // radius of the earth in km
  		const dLat = (lat2 - lat1) * (Math.PI / 180);
  		const dLon = (lon2 - lon1) * (Math.PI / 180);
 		const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) + Math.cos(lat1 * (Math.PI / 180)) * Math.cos(lat2 * (Math.PI / 180)) * Math.sin(dLon / 2) * Math.sin(dLon / 2);
  		const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  		const d = R * c;
  		return d;
}

navigator.geolocation.watchPosition(success, error);

function success (pos) {
  startLat = pos.coords.latitude;
  startLon = pos.coords.longitude;
  accuracy = pos.coords.accuracy;

  const url = `https://nominatim.openstreetmap.org/reverse?format=json&lat=${startLat}&lon=${startLon}`;

  fetch(url)
    .then(res => {
      if (res.status == 200) {
        return res.json();
      }
      throw new Error();
    })
    .then(data => {
      current_location = data.display_name;
    })
    .catch(error => {
      console.log(error);
    });

  // Remove existing marker and circle
  if (marker) {
    map.removeLayer(marker);
        		map.removeLayer(circle);
    		}

    		if (dMarker) {
    			map.removeLayer(dMarker);
    		}

    		marker = L.marker([startLat, startLon]).addTo(map);
    		circle = L.circle([startLat, startLon], { radius: accuracy }).addTo(map);

    		if (!zoomed) {
        		zoomed = map.fitBounds(circle.getBounds());
    		}

    		map.setView([startLat, startLon]);

  if (endLon && endLat) {
    drawRoute(startLat, startLon, endLat, endLon);
  }
}

function error (err) {
    		if (err.code === 1) {
        		alert('Please allow geolocation access');
    		} else {
        		alert('Cannot get current location');
   		}
}

searchInput.addEventListener('focus', () => {
  locations.style.display = 'block';
  locations.innerHTML = '';
});

searchInput.addEventListener('blur', (e) => {
  if (e.relatedTarget && !e.relatedTarget.classList.contains('destination')) {
    locations.style.display = 'none';
  }
});

searchInput.addEventListener('keyup', () => {
  const value = searchInput.value;
  if (value.length > 2) {
    locations.innerHTML = '';
    fetch(`https://nominatim.openstreetmap.org/search?q=${value}&format=json`)
    			.then(response => response.json())
    			.then(data => {
    				let locationsContent = '';
      				// Do something with the latitude and longitude
      				for (let i = 0; i < data.length; i++) {
      					d = distance(startLat, startLon, data[i].lat, data[i].lon);
      					locationsContent += `<li class="location" data-lat=${data[i].lat} data-lon=${data[i].lon} data-dest='${data[i].display_name}'><span class="l-span"><i class="fas fa-map-marker-alt icon"></i><span class="dist">${d.toFixed(2)}km</span></span>${data[i].display_name} </li>`;
      				}
      				if (locationsContent !== '') {
      					locations.innerHTML = locationsContent;
      				}
      				const locationItems = document.querySelectorAll('.location');
      				locationItems.forEach(item => {
          item.addEventListener('click', (e) => {
            endLon = e.target.getAttribute('data-lon');
            endLat = e.target.getAttribute('data-lat');
            locations.style.display = 'none';
            currentDest = e.target.getAttribute('data-dest');
            searchInput.value = currentDest;
            drawRoute(startLat, startLon, endLat, endLon);
          });
        });
    			})
    			.catch(error => console.log(error));
  }
});
