import { createRoot } from 'react-dom/client';

export const renderExample = () => {
    const root = createRoot(document.getElementById('react_root'));
    root.render(<h1>Hello World</h1>);
}
