import { useEffect, useReducer } from "react";

interface CountdownState {
	days: number;
	hours: number;
	minutes: number;
	seconds: number;
}

interface CountdownAction {
	type: string;
	payload: CountdownState;
}

const initialState: CountdownState = {
  days: 0,
  hours: 0,
  minutes: 0,
  seconds: 0,
};

const countdownReducer = (state: CountdownState, action: CountdownAction) => {
  switch (action.type) {
    case 'SET_COUNTDOWN':
      return action.payload;
    default:
      return state;
  }
};

export const useCountdown = (date: Date) => {

  const [countdown, dispatch] = useReducer(countdownReducer, initialState);

  const calculateTimeLeft = () => {
    const countdownDate = date.getTime();
    const now = new Date().getTime();
    const timeDifference = countdownDate - now;

    const days = Math.floor(timeDifference / (1000 * 60 * 60 * 24));

    const hours = Math.floor(
      (timeDifference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)
    );

    const minutes = Math.floor(
      (timeDifference % (1000 * 60 * 60)) / (1000 * 60)
    );
    const seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);

    dispatch({
      type: 'SET_COUNTDOWN',
      payload: { days, hours, minutes, seconds },
    });

  };

  useEffect(() => {
    const timer = setInterval(calculateTimeLeft, 1000);
    return () => clearInterval(timer);
  }, []);

  return {...countdown};

};
