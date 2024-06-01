import React from "react";
import PlayerNameBox from "./PlayerNameBox";

const JoinedList = (props: any) => {
  return (
    <div className="joinedplayerslist">
      <h2>Players joined: </h2>
      {[...props.joinedPlayers].map((person) => (
        <PlayerNameBox name={person} />
      ))}
    </div>
  );
};

export default JoinedList;
