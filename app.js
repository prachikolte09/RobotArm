import React, { useState } from 'react';
import axios from 'axios';

function App() {
    const [inputs, setInputs] = useState({
        height: '',
        width: '',
        length: '',
        mass: ''
    });
    const [response, setResponse] = useState(null);

    const handleChange = (event) => {
        const { name, value } = event.target;
        setInputs(prevInputs => ({ ...prevInputs, [name]: value }));
    };

    const handleSubmit = (event) => {
        event.preventDefault();
        axios.post("http://127.0.0.1:8000/sort_package/", inputs)
            .then(response => {
                console.log(response.data);
                setResponse(response.data);
            })
            .catch(error => {
                console.error("Error:", error);
            });
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <label>Height:
                    <input
                        type="number"
                        name="height"
                        value={inputs.height}
                        onChange={handleChange}
                    />
                </label>
                <label>Width:
                    <input
                        type="number"
                        name="width"
                        value={inputs.width}
                        onChange={handleChange}
                    />
                </label>
                <label>Length:
                    <input
                        type="number"
                        name="length"
                        value={inputs.length}
                        onChange={handleChange}
                    />
                </label>
                <label>Mass:
                    <input
                        type="number"
                        name="mass"
                        value={inputs.mass}
                        onChange={handleChange}
                    />
                </label>
                <button type="submit">Submit</button>
            </form>

            {response && (
                <div>
                    <h2>Response:</h2>
                    <pre>{JSON.stringify(response, null, 2)}</pre>
                </div>
            )}
        </div>
    );
}

export default App;
