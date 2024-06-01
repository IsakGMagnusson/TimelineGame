import React from "react";
import { CardData, Card_State, Class_Names } from "../../interfaces";

const Card = (props: any) => {
  function getCardClassFromStatus(card: CardData) {
    switch (card.state) {
      case Card_State.ACTIVE:
        return Class_Names.ACTIVE;
      case Card_State.LOCKED:
        return Class_Names.LOCKED;
      case Card_State.PLACED:
        return Class_Names.PLACED;
      case Card_State.ANIMATE:
        return Class_Names.ANIMATE;
      default:
        return "";
    }
  }

  return (
    <div>
      <div className={getCardClassFromStatus(props.card)}>
        <h2>{props.card.question}</h2>
      </div>
      <h2 className="active-cards-h2">
        {props.card.state == Card_State.ACTIVE
          ? props.activeCardDisplayDate
          : props.card.date}
      </h2>
    </div>
  );
};

export default Card;
