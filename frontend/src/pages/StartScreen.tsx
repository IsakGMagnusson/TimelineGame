// Importing modules
import React, { useState } from "react";
import "../App.css";
import { useNavigate } from "react-router-dom";

function App() {
  const [inputName, setInputName] = useState("");
  const [inputGameCode, setInputGameCode] = useState("");
  const [attemptedGameCode, setAttemptedGameCode] = useState("");
  const [isGameCodeValid, setIsGameCodeValid] = useState(true);

  const navigate = useNavigate();

  const changeInputName = (event: React.ChangeEvent<HTMLInputElement>) => {
    setInputName(event.target.value);
  };

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
      body: JSON.stringify({ gamecode: inputGameCode }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.isGameCodeValid)
          navigate("/Game", {
            state: { gameCode: inputGameCode, name: inputName },
          });
        else {
          setIsGameCodeValid(data.isGameCodeValid);
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
              onChange={changeInputName}
            />
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
        {isGameCodeValid ? "" : `No game with code "${attemptedGameCode}"`}
      </header>
    </div>
  );
}

export default App;
