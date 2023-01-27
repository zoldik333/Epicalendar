import React from 'react';
import './index.css';

function MyButton() {
    return (
        <>
            <button>I'm a button</button>
        </>
    );
}

export default function MyApp() {
    return (
        <>
            <div className="banner">
                <h1>Epicalendar</h1>
                <MyButton />
            </div>
        </>
    );
}