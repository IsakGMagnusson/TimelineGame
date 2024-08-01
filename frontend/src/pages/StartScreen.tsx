// Importing modules
import React, { useState } from "react";
import "../App.css";
import { useNavigate } from "react-router-dom";
import { useSetName } from "../hooks/UseSetName";

function App() {
  //const [inputName, setInputName] = useState("");
  const [name, generateRandomName, readName] = useSetName();

  const [inputGameCode, setInputGameCode] = useState("");
  const [attemptedGameCode, setAttemptedGameCode] = useState("");
  const [joinErrorCode, setJoinErrorCode] = useState("");

  const navigate = useNavigate();

  const changeGameCode = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputGameCode(event.target.value);
  };

  const createGame = () => {
    navigate("/HostGame");
  };

  const joinGame = () => {
    fetch(`/JoinGame`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ gamecode: inputGameCode, name: name }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.joinError.length == 0)
          navigate("/Game", {
            state: {
              gameCode: inputGameCode,
              name: name,
            },
          });
        else {
          setJoinErrorCode(data.joinError);
          setAttemptedGameCode(inputGameCode);
        }
      });
  };

  return (
    <div className="App">
      <header className="App-header">
        <div>
          <button
            onClick={() => {
              createGame();
            }}
          >
            Create Game
          </button>
          <div>
            Username:
            <input
              autoComplete="off"
              type="text"
              id="fname"
              name="fname"
              onChange={(e) => readName(e.target.value)}
              value={name}
            />
            <button onClick={generateRandomName}>random</button>
          </div>
          <div>
            Gamecode:
            <input
              autoComplete="off"
              type="text"
              id="fname"
              name="fname"
              onChange={changeGameCode}
            />
          </div>
          <button
            onClick={() => {
              joinGame();
            }}
          >
            Join Game
          </button>
        </div>
        {joinErrorCode}
      </header>
    </div>
  );
}

export default App;
