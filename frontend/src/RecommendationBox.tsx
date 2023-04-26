import React, { useRef, useEffect } from 'react';

/**
 * Calculate the position of the cursor relative to the center of the element.
 * @param element The element to calculate the cursor position relative to
 * @param event The mouse event which contains the current cursor position
 * @returns {x: number, y: number}
 */
const calculateCursorPosition = (element: HTMLElement, event: MouseEvent) => {
    const rect = element.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    const x = event.clientX - centerX;
    const y = centerY - event.clientY;
    return { x, y };
}

/**
 * Required properties to display a recommendation box.
 * @param symbol The stock's symbol
 * @param currentPrice The stock's current price
 * @param recommendation The stock's recommendation (buy, hold, sell)
 * @param sentiment The stock's sentiment (what percentage of analysts agree with the recommendation)
 */
interface RecommendationBoxProps {
    symbol: string;
    currentPrice: number;
    recommendation: string;
    sentiment: number;
}

/**
 * A small box that displays a stock's symbol, current price, recommendation, and sentiment.
 * @see RecommendationBoxProps
 * 
 * -------------------------------
 * @param symbol The stock's symbol
 * @param currentPrice The stock's current price
 * @param recommendation The stock's recommendation (buy, hold, sell)
 * @param sentiment The stock's sentiment (what percentage of analysts agree with the recommendation)
 * 
 * @returns A rounded rectangle with the stock's symbol, current price, recommendation, and sentiment neatly displayed
 */
const RecommendationBox: React.FunctionComponent<RecommendationBoxProps> = ({ symbol, currentPrice, recommendation, sentiment }) => {
    const recommendationBoxRef = useRef<HTMLButtonElement>(null);

    /**
     * Update the position of the cursor on the recommendation box.
     * This is used to create a rainbow gradient effect on hover.
     * 
     * When the component is unmounted (i.e. when the user leaves the page), remove the event listeners.
     */
    useEffect(() => {
        if (recommendationBoxRef.current) {
            recommendationBoxRef.current.addEventListener('mousemove', (e) => {
                const { x, y } = calculateCursorPosition(recommendationBoxRef.current!, e);
                recommendationBoxRef.current!.style.setProperty('--x', `${x}`);
                recommendationBoxRef.current!.style.setProperty('--y', `${y}`);
            });
            recommendationBoxRef.current.addEventListener('mouseleave', () => {
                recommendationBoxRef.current!.style.setProperty('--x', `0`);
                recommendationBoxRef.current!.style.setProperty('--y', `0`);
            });
        }

        return () => {
            if (recommendationBoxRef.current) {
                recommendationBoxRef.current!.removeEventListener('mousemove', () => { });
                recommendationBoxRef.current!.removeEventListener('mouseleave', () => { });
            }
        }
    });

    /**
     * Create a locale currency formatter which formats the stock's current price as USD (e.g. $123.45)
     */
    const currencyFormatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
    });

    return (
        // Open the stock's Yahoo Finance page in a new tab when the user clicks on the recommendation box
        <a href={`https://finance.yahoo.com/quote/${symbol}`} className="recommendation-link" target="_blank" rel="noopener noreferrer">
            <button className="recommendation-box" ref={recommendationBoxRef}>
                <div className="inner">
                    <div className="stock-info">
                        <div className="left">
                            <span className="symbol">{symbol}</span>
                            <span className="current-price">{currencyFormatter.format(currentPrice)}</span>
                        </div>
                        <div className="right">
                            <span className={`recommendation ${recommendation?.toLowerCase()}`}>{recommendation}</span>
                            <span className="accuracy">{sentiment.toFixed(0)}% Sentiment</span>
                        </div>
                    </div>
                </div>
            </button>
        </a>
    );
}

export default RecommendationBox;