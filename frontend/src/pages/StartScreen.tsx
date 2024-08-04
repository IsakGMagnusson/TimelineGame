// Importing modules
import React, { useState } from "react";
import "../App.css";
import { useNavigate } from "react-router-dom";
import { useSetName } from "../hooks/UseSetName";

function App() {
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
    <div className="startscreen">
      <div className="creategame-container">
        <button
          className="create-game"
          onClick={() => {
            createGame();
          }}
        >
          Create Game
        </button>
      </div>
      <div className="joingame-container">
        <div className="input-and-label">
          <div className="join-text">Code</div>
          <input
            className="join-input"
            autoComplete="off"
            type="text"
            id="fname"
            name="fname"
            onChange={changeGameCode}
          />
        </div>
        <div className="input-and-label">
          <div className="join-text">Name</div>
          <div className="input-and-button">
            <input
              className="join-input"
              autoComplete="off"
              type="text"
              id="fname"
              name="fname"
              onChange={(e) => readName(e.target.value)}
              value={name}
            />
            <button className="random-name-button" onClick={generateRandomName}>
              ?
            </button>
          </div>
        </div>
        <button
          className="join-game"
          onClick={() => {
            joinGame();
          }}
        >
          Play
        </button>
        <div className="error-text"> {joinErrorCode}</div>
      </div>
    </div>
  );
}

export default App;
