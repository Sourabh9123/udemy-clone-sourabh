import axios from "axios"
import './App.css';
import useRazorpay from "react-razorpay";

function App() {
  const [Razorpay] = useRazorpay();
  const token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE2MDcxOTEzLCJpYXQiOjE3MTAwNzE5MTMsImp0aSI6IjJlNWJkMjQxMWEyNTQxZjNhNzgxM2Y3NmVjZWRlZWY2IiwidXNlcl9pZCI6IjQ0ODMzMzQ2LTNjNWMtNDBjZi04ODk3LTExMDExZTE0NTJhOSJ9.elOVxoi-YnxCgVT5jlCMiKqWVO-hx4AF6b3kgeGcfKc"
  
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

  const complete_payment = (razorpay_payment_id,razorpay_order_id,razorpay_signature,current_amount,course_id) => {
    axios.post('http://127.0.0.1:8000/api/cart/payment/success/',  {
      
      "payment_id":razorpay_payment_id,
      "order_id": razorpay_order_id, 
      "signature": razorpay_signature,
      "amount" : current_amount,
      "course_id" : course_id
      
    
    },
    { headers: headers }
    )
      .then((response) => {
        console.log("inside complete payment")
        console.log(response.data);
        if (response.data.type === "success") {
          console.log("payment success");
        }
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
        console.log("data is here",response.data);
        
        const course_id = response.data.course_id;
        

        // const order_id = response.data.payment.id
        // const current_amount = response.data.order.amount
        const order_id = response.data.order_id; // Correct way to access order_id
        const current_amount = response.data.amount;
        

   

        const options = {
        key: "rzp_test_DqyEDw9vF6Y4kA", // Enter the Key ID generated from the Dashboard
        
        name: "Acme Corp",
        description: "Test Transaction",
        image: "https://example.com/your_logo",
        order_id: order_id, //This is a sample Order ID. Pass the `id` obtained in the response of createOrder().
        handler: function (response) {
          console.log("before calling the complete payment")
         
          complete_payment(response.razorpay_payment_id,response.razorpay_order_id ,response.razorpay_signature, current_amount,course_id)
          
          
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
