// Importing modules
import { useState, useEffect } from "react";
import "../App.css";

import { io } from "socket.io-client";
import { useLocation } from "react-router-dom";
import React from "react";
import Controller from "../components/Controller/Controller";

const socket = io({ autoConnect: false });

function Game() {
  const location = useLocation();
  const [gameCode, setGameCode] = useState(location.state.gameCode);
  const [name, setPlayerName] = useState(location.state.name);
  const [isGameStarted, setIsGameStarted] = useState(false);
  const [timeline, setTimeline] = useState([]);
  const [isMyTurn, setIsMyTurn] = useState(false);
  const [disconnectedPlayerNames, setDisconnectedPlayerNames] = useState([]);

  useEffect(() => {
    socket.connect();
    socket.on("connect", function () {
      socket.emit("user_join", gameCode, name);
    });
  }, []);

  useEffect(() => {
    socket.on("game_start", function (data) {
      setTimeline(data.timeline);
      setIsGameStarted(true);
    });
  }, []);

  useEffect(() => {
    socket.on("new_turn", function (data) {
      setIsMyTurn(data.isMyTurn);
    });
  }, []);

  useEffect(() => {
    socket.on("reconnect", function (data) {
      setDisconnectedPlayerNames(data.disconnectedPlayers);
      setIsGameStarted(true);
    });
  }, []);

  useEffect(() => {
    socket.on("send_disconnected_playernames", function (data) {
      setDisconnectedPlayerNames(data.playernames);
    });
  }, []);

  useEffect(() => {
    socket.on("server_send_ping", function () {
      socket.emit("user_send_pong", gameCode, name);
    });
  }, [name]);

  useEffect(() => {
    socket.on("reconnect_as_player", function (data) {
      setIsMyTurn(data.isMyTurn);
    });
  }, []);

  const reconnect = (name: string) => {
    setPlayerName(name);
    socket.emit("reconnect", gameCode, name);
  };

  return (
    <div className="fullwidth">
      {isGameStarted ? (
        <>
          {disconnectedPlayerNames.length > 0 ? (
            <>
              <div className="active-cards">
                {[...disconnectedPlayerNames].map((name: string) => (
                  <div>
                    <button
                      onClick={() => {
                        reconnect(name);
                      }}
                    >
                      Connect as {name}
                    </button>
                  </div>
                ))}
              </div>
            </>
          ) : (
            <>
              {isMyTurn ? (
                <Controller socket={socket} gameCode={gameCode} />
              ) : (
                <h1>not your turn!</h1>
              )}
            </>
          )}
        </>
      ) : (
        <h1>Game not started!</h1>
      )}
    </div>
  );
}

export default Game;
