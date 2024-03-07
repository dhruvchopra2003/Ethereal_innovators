// let obj;
// const submit = document.getElementById('submit');
// const certi = document.getElementById('certification');

// submit.addEventListener('click', () => {
//     let title = document.getElementById('title').value;
//     let description = document.getElementById('description').value;
//     let price = document.getElementById('price').value;
//     let categoty = document.getElementById('category').value;
//     let image = document.getElementById('image').value;
//     let certival = certi.value;
//     obj = { title, description, price, categoty, image, certival };
//     console.log(obj);
//     // console.log(image);
// })


let obj;
const submit = document.getElementById('submit');
const certi = document.getElementById('certification');

submit.addEventListener('click', () => {
    // title = data.get('product_title')
    // image = data.get('product_image')
    // desc = data.get('product_description')
    // id = data.get('product_id')
    // certival = data.get('product_certi')

    let product_title = document.getElementById('title').value;
    let product_description = document.getElementById('description').value;
    let price = document.getElementById('price').value;
    let category = document.getElementById('category').value;
    let product_image = document.getElementById('image').value;
    let certival = certi.checked ? 1 : 0;

    // Create the object with product data
    obj = { product_title, product_description, price, category, product_image, certival };

    // Send a POST request to your Flask API endpoint
    fetch('http://127.0.0.1:5000/rank', {
        method: 'POST', // Specify POST method
        headers: {
            'Content-Type': 'application/json' // Set content type to JSON
        },
        body: JSON.stringify(obj) // Stringify the object before sending
    })
        .then(response => response.json()) // Parse response as JSON
        .then(data => {
            console.log('Success:', data); // Handle successful response (optional)
        })
        .catch(error => {
            console.error('Error:', error); // Handle errors (important)
        });
});
