import React, { useEffect, useState } from "react";

const TurnDecisionController = (props: any) => {
  const [touchStart, setTouchStart] = useState<number>(0);
  const [touchEnd, setTouchEnd] = useState<number | null>(0);

  enum Selection {
    NO_SELECTION = "no_selection",
    DRAW_CARD = "draw_card",
    NEXT_TURN = "next_turn",
  }

  const [selection, setSelection] = useState<Selection>(Selection.NO_SELECTION);

  const minSwipeDistance = 80;

  const onTouchStart = (e: React.TouchEvent<HTMLElement>) => {
    setTouchEnd(null); // otherwise the swipe is fired even with usual touch events
    setTouchStart(e.targetTouches[0].clientX);
  };

  const onTouchMove = (e: React.TouchEvent<HTMLElement>) => {
    setTouchEnd(e.targetTouches[0].clientX);
    setSelectionStatus();
  };

  const onTouchEnd = () => {
    if (Selection.DRAW_CARD == selection) DrawCard();
    if (Selection.NEXT_TURN == selection) GoNextTurn();
  };

  const setSelectionStatus = () => {
    if (!touchStart || !touchEnd) return;
    const distance = touchStart - touchEnd;
    const isLeftSwipe = distance > minSwipeDistance;
    const isRightSwipe = distance < -minSwipeDistance;

    if (isLeftSwipe) setSelection(Selection.DRAW_CARD);
    else if (isRightSwipe) setSelection(Selection.NEXT_TURN);
    else setSelection(Selection.NO_SELECTION);
  };

  const GoNextTurn = () => {
    props.socket.emit("go_next_turn", props.gameCode);
  };

  const DrawCard = () => {
    props.socket.emit("draw_card", props.gameCode);
  };

  return (
    <>
      <div
        className="swipe-div"
        onTouchStart={onTouchStart}
        onTouchMove={onTouchMove}
        onTouchEnd={onTouchEnd}
      >
        <button
          onClick={() => {
            DrawCard();
          }}
        >
          Draw
        </button>
        <button
          onClick={() => {
            GoNextTurn();
          }}
        >
          Next
        </button>
        <div className="swipe instructions">
          <h2
            className={
              selection == Selection.DRAW_CARD
                ? "swipe h2 selected"
                : "swipe h2"
            }
          >
            Draw Card
          </h2>
          <h2 className="swipe h2">[swipe]</h2>
          <h2
            className={
              selection == Selection.NEXT_TURN
                ? "swipe h2 selected"
                : "swipe h2"
            }
          >
            Next Turn
          </h2>
        </div>
      </div>
    </>
  );
};

export default TurnDecisionController;
