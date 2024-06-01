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
  const [timeline, setTimeline] = useState([]);
  const [isMyTurn, setIsMyTurn] = useState(false);

  useEffect(() => {
    socket.connect();
    socket.on("connect", function () {
      socket.emit("user_join", gameCode, name);
    });
  }, []);

  useEffect(() => {
    socket.on("game_start", function (data) {
      setTimeline(data.timeline);
    });
  }, []);

  useEffect(() => {
    socket.on("new_turn", function (data) {
      setIsMyTurn(data.isMyTurn);
    });
  }, []);

  useEffect(() => {
    socket.on("server_send_ping", function () {
      socket.emit("user_send_pong", gameCode, name);
    });
  }, []);

  return (
    <div className="fullwidth">
      {timeline.length != 0 ? (
        <>
          {isMyTurn ? (
            <Controller socket={socket} gameCode={gameCode} />
          ) : (
            <h1>not your turn!</h1>
          )}
        </>
      ) : (
        <h1>Game not started!</h1>
      )}
    </div>
  );
}

export default Game;
