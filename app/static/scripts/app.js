window.onload = (event) => {
    console.log("HELLO OdddUYT THERE!!")
    console.log('page is fully loaded');
    console.log(document.querySelector('h1').textContent)
    document.querySelector('h1').textContent = 'Hello from Beans!'
    console.log(document.querySelector('h1').textContent)


    const userAction = async () => {
        const response = await fetch('http://localhost:8000/test');
        const myJson = await response.json(); //extract JSON from the http response
        // do something with myJson
        await console.log(myJson)
    }
    userAction()
};