import React from "react";

const WinScreen = (props: any) => {
  return (
    <div className="turn-box">
      <h2>Player won: {props.name}</h2>
    </div>
  );
};

export default WinScreen;
