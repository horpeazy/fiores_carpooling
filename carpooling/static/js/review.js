const endrideEl = document.querySelector('.end-ride-btn');
const reviewEl = document.querySelector('.review-wrapper');
const closeBtn = document.querySelector('.close-review ');
const lcloseBtn = document.querySelector('.l-close-review');
const creviewBtn = document.querySelector('.c-review-btn');
const lreviewBtn = document.querySelectorAll('.l-review-btn');
const lreviewEl = document.querySelector('.l-review-wrapper');
let trip_id;
let user_id;

if (endrideEl) {
	endrideEl.addEventListener('click', (e) => {
		e.preventDefault();
		reviewEl.style.display = 'flex';
	});
}

closeBtn.addEventListener('click', (e) => {
	e.preventDefault();
	reviewEl.style.display = "none";
});

lcloseBtn.addEventListener('click', (e) => {
	e.preventDefault();
	alert("Yesss")
	lreviewEl.style.display = "none";
});

lreviewBtn.forEach((element) => {
	element.addEventListener('click', (e) => {
		e.preventDefault();
		user_id = e.target.getAttribute('data-id');
		trip_id = e.target.getAttribute('data-trip');
		lreviewEl.style.display = 'flex';
	});
});

creviewBtn.addEventListener('click', (e) => {
	e.preventDefault();
	console.log("yes")
	review = document.querySelector('.review-text').value;
	fetch('/create-review/', {
		method: "POST",
		body: JSON.stringify({
			review: review,
			user_id: user_id,
			trip_id: trip_id
		})
	})
	.then(res => {
		if (!res.ok) {
			throw new Error("Could not create review");
		} 
		return res.json()
	})
	.then(data => {
		if (data.message == "Created Successfully") {
			window.location = `/trips/${trip_id}`;
		}
	})
	.catch(error => console.log(error))
});
