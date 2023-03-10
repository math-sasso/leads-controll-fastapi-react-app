import React, {useState, useEffect, useContext} from "react";
import Header from "./components/Header";

import Register from "./components/Register";
import { UserContext } from "./context/UserContext";
import Login from "./components/Login";
import Table from "./components/Table";

const App = () =>{
  const [message, setMessage] = useState("");
  const [token, ] = useContext(UserContext)

  const getWelcomeMessage = async () => {
    const requestOptions = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    };

    const response = await fetch("/api", requestOptions);
    const data = await response.json();

    if (!response.ok) {
      console.log("something messed up");
    } else {
      setMessage(data.message);
    }
  };

  useEffect(() => {
    getWelcomeMessage();
  }, []);
  
  return (
    <>
    <Header title={message}/>
    <div className="columns">
      <div className="column m-5 tw">
      {!token ? (
            <div className="columns">
              <Register /> 
              <Login/>
            </div>
          ) : (
            <Table/>
      )}
      </div>
    </div>
    </>
    );
};

export default App;
