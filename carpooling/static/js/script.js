			const sidebar = document.querySelector('#sidebar');
			const toggleButton = document.querySelector('#sidebar-toggle');
			const facultiesEl = document.querySelector(".faculties");
			const searchEl = document.querySelector(".search");
			const faculties = [ 
				{ 
					name: "EDEBİYAT FAKÜLTESİ", 
					latLng: [39.87234, 32.73787],
					departments: [
						{ name: "Alman Dili ve Edebiyatı", latLng: [39.87234, 32.73787], icon: "icon.png" },
						{ name: "Amerikan Kültürü ve Edebiyatı", latLng: [39.87203, 32.73766], icon: "icon.png" },
						{ name: "Antropoloji", latLng: [39.87234, 32.73787], icon: "icon.png" },
						{ name: "Arkeoloji", latLng: [ 39.87308, 32.73689 ], icon: "icon.png" },
						{ name: "Bilgi ve Belge Yönetimi", latLng: [39.87221, 32.73726], icon: "icon.png" },
						{ name: "Felsefe", latLng: [39.87203, 32.73766], icon: "icon.png" },
						{ name: "Fransız Dili ve Edebiyatı", latLng: [39.87234, 32.73787], icon: "icon.png" },
						{ name: "İngiliz Dilbilimi", latLng: [39.87276, 32.73766 ], icon: "icon.png" },
						{ name: "İngiliz Dili ve Edebiyatı", latLng: [39.87234, 32.73787], icon: "icon.png" },
						{ name: "Mütercim-Tercümanlık", latLng: [39.87322, 32.73747], icon: "icon.png" },
						{ name: "Psikoloji", latLng: [39.87276, 32.73767], icon: "icon.png" },
						{ name: "Sanat Tarihi", latLng: [39.87262, 32.73708], icon: "icon.png" },
						{ name: "Sosyoloji", latLng: [39.87221, 32.73726], icon: "icon.png" },
						{ name: "Tarih", latLng: [39.87322, 32.73747], icon: "icon.png" },
						{ name: "Türk Dili ve Edebiyatı", latLng: [39.87203, 32.73761], icon: "icon.png" }
					]
				},
				{ 
					name: "MÜHENDİSLİK FAKÜLTESİ", 
					latLng: [39.87154, 32.73655],
					departments: [
						{ name: "Bilgisayar Mühendisliği", latLng: [39.87154, 32.73655], icon: "icon.png" },
						{ name: "Çevre Mühendisliği", latLng: [39.87088, 32.73684], icon: "icon.png" },
						{ name: "Elektrik - Elektronik Mühendisliği", latLng: [39.86982, 32.73459], icon: "icon.png" },
						{ name: "Endüstri Mühendisliği", latLng: [39.86824, 32.7416], icon: "icon.png" },
						{ name: "Fizik Mühendisliği", latLng: [39.86931, 32.73408], icon: "icon.png" },
						{ name: "Geomatik Mühendisliği", latLng: [39.86567, 32.73384 ], icon: "icon.png" },
						{ name: "Gıda Mühendisliği", latLng: [39.86649, 32.73758 ], icon: "icon.png" },
						{ name: "İnşaat Mühendisliği", latLng: [39.86407, 32.7343], icon: "icon.png" },
						{ name: "Jeoloji Mühendisliği", latLng: [39.87088, 32.73684], icon: "icon.png" },
						{ name: "Hidrojeoloji Mühendisliği", latLng: [39.87088, 32.73684], icon: "icon.png" },
						{ name: "Kimya Mühendisliği", latLng: [39.86906, 32.73709], icon: "icon.png" },
						{ name: "Maden Mühendisliği", latLng: [39.87088, 32.73684], icon: "icon.png" },
						{ name: "Makine Mühendisliği", latLng: [39.86372, 32.73436], icon: "icon.png" },
						{ name: "Nükleer Enerji Mühendisliği", latLng: [39.86931, 32.73408], icon: "icon.png" },
						{ name: "Yapay Zeka Mühendisliği", latLng: [39.87154, 32.73655], icon: "icon.png" }
					]
				},
				{ 
					name: "İKTİSADİ İDARİ BİLİMLER FAKÜLTESİ", 
					latLng: [39.86524, 32.73592],
					departments: [
						{ name: "Aile ve Tüketici Bilimleri Bölümü", latLng: [ 39.86524, 32.73592 ], icon: "icon.png" },
						{ name: "İktisat Bölümü", latLng: [ 39.86524, 32.73592 ], icon: "icon.png" },
						{ name: "Maliye Bölümü", latLng: [ 39.86524, 32.73592 ], icon: "icon.png" },
						{ name: "Siyaset Bilimi ve Kamu Yönetimi Bölümü", latLng: [ 39.86524, 32.73592 ], icon: "icon.png" },
						{ name: "Sosyal Hizmet Bölümü", latLng: [ 39.86524, 32.73592 ], icon: "icon.png" },
						{ name: "Sağlık Yönetimi Bölümü", latLng: [ 39.86524, 32.73592 ], icon: "icon.png" },
						{ name: "Uluslararası İlişkiler Bölümü", latLng: [ 39.86524, 32.73592 ] , icon: "icon.png" },
						{ name: "İşletme Bölümü", latLng: [ 39.86524, 32.73592 ], icon: "icon.png" }
					]
				},
				{ 
					name: "GÜZEL SANATLAR FAKÜLTESİ", 
					latLng: [39.86611, 32.73525],
					departments: [
						{ name: "Grafik Bölümü", latLng: [39.86611, 32.73525], icon: "icon.png" },
						{ name: "Heykel Bölümü", latLng: [ 39.86678, 32.73646 ], icon: "icon.png" },
						{ name: "İç Mimarlık ve Çevre Tasarımı Bölümü", latLng: [39.86611, 32.73525], icon: "icon.png" },
						{ name: "Resim Bölümü", latLng: [39.86611, 32.73525], icon: "icon.png" },
						{ name: "Seramik ve Cam Bölümü", latLng: [39.86611, 32.73525], icon: "icon.png" }
					]
				},
				{ 
					name: "EĞİTİM FAKÜLTESİ", 
					latLng: [39.86424, 32.73604],
					departments: [
						{ name: "Bilgisayar ve Öğretim Teknolojileri Eğitimi Bölümü", latLng: [39.86424, 32.73604], icon: "icon.png" },
						{ name: "Eğitim Bilimleri Bölümü", latLng: [39.86424, 32.73604], icon: "icon.png" },
						{ name: "Matematik ve Fen Bilimleri Eğitimi Bölümü", latLng: [39.86424, 32.73604], icon: "icon.png" },
						{ name: "Özel Eğitim Bölümü", latLng: [39.86424, 32.73604], icon: "icon.png" },
						{ name: "Türkçe ve Sosyal Bilimler Eğitimi Bölümü", latLng: [39.86424, 32.73604], icon: "icon.png" },
						{ name: "Temel Eğitim Bölümü", latLng: [39.86424, 32.73604], icon: "icon.png" },
						{ name: "Yabancı Diller Eğitimi Bölümü", latLng: [39.86498, 32.73529] , icon: "icon.png" }
					]
				},
				{ 
					name: "FEN FAKÜLTESİ", 
					latLng: [39.87029, 32.73697],
					departments: [
						{ name: "Aktüerya Bilimleri Bölümü", latLng: [39.87029, 32.73697], icon: "icon.png" },
						{ name: "Biyoloji Bölümü", latLng: [39.87146, 32.73548 ], icon: "icon.png" },
						{ name: "İstatistik Bölümü", latLng: [39.86983, 32.73675], icon: "icon.png" },
						{ name: "Kimya Bölümü", latLng: [39.86909, 32.73637 ], icon: "icon.png" },
						{ name: "Matematik Bölümü", latLng: [39.86954, 32.737], icon: "icon.png" }
					]
				}, 
				{ 
					name: "İLETİŞİM FAKÜLTESİ", 
					latLng: [39.87277, 32.73769],
					departments: [
						{ name: "İletişim Bilimleri Bölümü", latLng: [39.87277, 32.73769], icon: "icon.png" },
						{ name: "Radyo, TV ve Sinema Bölümü", latLng: [39.87277, 32.73769], icon: "icon.png" },
					]
				},
				{ 
					name: "SPOR BİLİMLERİ FAKÜLTESİ", 
					latLng: [39.87224, 32.73087],
					departments: [
						{ name: "Beden Eğitimi ve Spor Öğretmenliği Bölümü", latLng: [39.87224, 32.73087], icon: "icon.png" },
						{ name: "Egzersiz ve Spor Bilimleri Bölümü", latLng: [39.87224, 32.73087], icon: "icon.png" },
						{ name: "Rekreasyon Bölümü", latLng: [39.87224, 32.73087], icon: "icon.png" },
					]
				}, 
				{ 
					name: "HUKUK FAKÜLTESİ", 
					latLng: [39.86334, 32.73216],
					departments: [
						{ name: "Özel Hukuk Bölümü", latLng: [39.86334, 32.73216], icon: "icon.png" },
						{ name: "Kamu Hukuku Bölümü", latLng: [39.86334, 32.73216], icon: "icon.png" },
					]
				}
			];
			
			// Initialize and display map
			// Initialize and display map
mapboxgl.accessToken = 'pk.eyJ1IjoiaG9ycGVhenkiLCJhIjoiY2xmNjFuOGJyMWk0bzN2cjBzZno0NXNmdCJ9.aEgc6K_vrA2mctaeIFzBrg';
const map = new mapboxgl.Map({
  container: 'map',
  style: 'mapbox://styles/mapbox/streets-v11',
  center: [32.73637, 39.86909],
  zoom: 15
});

map.addControl(new mapboxgl.NavigationControl(), 'top-right');

const markerLayer = new mapboxgl.Marker().setLngLat([0, 0]).addTo(map);
let markers = []

const markerImage = new Image(32, 32);
markerImage.src = "/static/images/icon.png";

map.on('load', function() {
  addMarkers()
  
});


function addMarkers() {
  faculties.forEach((faculty) => {
    const departments = faculty.departments;
    departments.forEach((department) => {
      const el = document.createElement("div");
      el.className = "marker";
      const marker = new mapboxgl.Marker(el, {
      	anchor: "bottom",
      	pitchAlignment: "auto",
      	rotationAlignment: "auto",
      }).setLngLat([department.latLng[1], department.latLng[0]])
        .setPopup(new mapboxgl.Popup({ offset: [0, -90]}).setHTML(department.name))
        .addTo(map);
      markers.push(marker);
    });
  });
}

function showFaculty(faculty) {
  const facultyLocation = [faculty.latLng[1], faculty.latLng[0]];
  map.flyTo({
    center: facultyLocation,
    zoom: 17,
    essential: true
  });
}

			
			function toTitleCase(str) {
  				return str.replace(/\w\S*/g, function(txt){
    					return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
  				});
			}
			
			function addPanel(items) {
  items.forEach((item) => {
    const facultyEl = document.createElement("div");
    facultyEl.classList.add('faculty');
    facultyEl.textContent = toTitleCase(item.name);
    facultyEl.onclick = () => {
      showFaculty(item);
      const lngLat = [item.latLng[1], item.latLng[0]];
      new mapboxgl.Popup({ offset: 90 })
      	.setLngLat(lngLat)
      	.setHTML(item.name)
      	.addTo(map);
      for (let i = 0; i < markers.length; i++) {
      	const marker = markers[i];
      	const markerObj = marker.getLngLat()
      	const markerLngLat = [markerObj.lng, markerObj.lat]
      	if ( markerLngLat[0] === lngLat[0] && markerLngLat[1] === lngLat[1] ) {
      		marker.fire("click");
      		break;
      	}
      }
      
    };
    facultiesEl.appendChild(facultyEl);
  });
}


			toggleButton.addEventListener('click', () => {
				sidebar.classList.toggle('open');
				toggleButton.classList.toggle('open');
			});
			
			searchEl.addEventListener('keyup', (e) => {
  				searchTerm = e.target.value.toLowerCase();
  				const result = [];
  				if (searchTerm.length > 1) {
    					for (const faculty of faculties) {
      						if (faculty.name.toLowerCase().includes(searchTerm)) {
        						result.push(faculty);
      						}
      						for (const department of faculty.departments) {
        						if (department.name.toLowerCase().includes(searchTerm)) {
          							result.push(department);
        						}
      						}
    					}
    					facultiesEl.innerHTML = "";
    					if (result.length > 0) {
      						addPanel(result);
    					}
  				} else {
    					facultiesEl.innerHTML = "";
    					addPanel(faculties);
  				}
			});


			// add faculties and markers
			addPanel(faculties);
			
