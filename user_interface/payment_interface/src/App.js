import axios from "axios"
import './App.css';
import useRazorpay from "react-razorpay";

function App() {
  const [Razorpay] = useRazorpay();
  const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA3NDczNDcwLCJpYXQiOjE3MDc0NjAyNzAsImp0aSI6ImE0MTg3YzI1OGFlNjQ4ZWZhOTA4MzVlZmI4NjZjYWViIiwidXNlcl9pZCI6IjBjZTQ1ZGZkLWY1NDctNDQyMi1hMGU3LTVmYTY4Zjk0NjU3NiJ9.XLHpvIhNkeJ3MHMkXQIeCIBa_7XRejTV2RNkU-cUBBk";
  const data = {
    firstName: 'Fred',
    lastName: 'Flintstone'
  };

  
  // Define the headers with the Bearer token
  const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json' // Set the content type if needed
  };
  
  console.log("this is before hitting api")

  const complete_payment = (razorpay_payment_id,razorpay_order_id,razorpay_signature,current_amount) => {
    axios.post('http://127.0.0.1:8000/api/cart/buy/', {
      
      "payment_id":razorpay_payment_id,
      "order_id": razorpay_order_id, 
      "signature": razorpay_signature,
      "amount" :current_amount
    
    })
      .then((response) => {
        console.log(response.data);
        console.log("function inside fun ")
        console.log(current_amount, "current amt")
      }) 
      .catch(error => {
        console.log(error);
        console.log("inside error");

      });
  };

  

  // Make the POST request using an arrow function
  const postData = () => {
    axios.post('http://127.0.0.1:8000/api/cart/buy/', data, { headers: headers })
      .then(response => {
        console.log(response.data);
        console.log(response.data.order.amount)
       const order_id = response.data.payment.id
       const current_amount = response.data.order.amount
   

        const options = {
        key: "rzp_test_DqyEDw9vF6Y4kA", // Enter the Key ID generated from the Dashboard
        
        name: "Acme Corp",
        description: "Test Transaction",
        image: "https://example.com/your_logo",
        order_id: order_id, //This is a sample Order ID. Pass the `id` obtained in the response of createOrder().
        handler: function (response) {
     
         
          complete_payment(response.razorpay_payment_id,response.razorpay_order_id ,response.razorpay_signature, current_amount)
          
          
        },
        prefill: { 
          name: "Sourabh Das",
          email: "skd@gmail.com",
          contact: "8444869123",
        },
        notes: {
          address: "Razorpay Corporate Office",
        },
        theme: {
          color: "#3399cc",
        },
      };
    
      const rzp1 = new Razorpay(options);
    
      rzp1.on("payment.failed", function (response) {
        alert(response.error.code);
        alert(response.error.description);
        alert(response.error.source);
        alert(response.error.step);
        alert(response.error.reason);
        alert(response.error.metadata.order_id);
        alert(response.error.metadata.payment_id);
      });
    
      rzp1.open();


      })
      .catch(error => {
        console.log(error);
      });
  };
 
  
  return (
    <>
    
    <button type="button" onClick={postData} className="btn btn-primary mx-2">Payment</button> 

    
    </>
  );
}

export default App;
