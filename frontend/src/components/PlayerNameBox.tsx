import React from "react";

const PlayerNameBox = (props: any) => {
  return (
    <div className="playerbox">
      <h2>{props.name}</h2>
    </div>
  );
};

export default PlayerNameBox;
