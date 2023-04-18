import React, { useRef, useEffect } from 'react';

const calculateCursorPosition = (element: HTMLElement, event: MouseEvent) => {
    const rect = element.getBoundingClientRect();
    const centerX = rect.left + rect.width / 2;
    const centerY = rect.top + rect.height / 2;
    const x = event.clientX - centerX;
    const y = centerY - event.clientY;
    return { x, y };
}

interface RecommendationBoxProps {
    symbol: string;
    currentPrice: number;
    recommendation?: string;
    accuracy?: number;
}

const RecommendationBox: React.FunctionComponent<RecommendationBoxProps> = ({ symbol, currentPrice, recommendation, accuracy }) => {
    const recommendationBoxRef = useRef<HTMLButtonElement>(null);

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

    const currencyFormatter = new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
    });

    return (
        <button className="recommendation-box" ref={recommendationBoxRef}>
            <div className="inner">
                <div className="stock-info">
                    <div className="left">
                        <span className="symbol">{symbol}</span>
                        <span className="current-price">{currencyFormatter.format(currentPrice)}</span>
                    </div>
                    <div className="right">
                        <span className={`recommendation ${recommendation?.toLowerCase()}`}>{recommendation}</span>
                        <span className="accuracy">{accuracy}% Sentiment</span>
                    </div>
                </div>
            </div>
        </button>
    );
}

export default RecommendationBox;