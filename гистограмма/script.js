document.getElementById('fileInput').addEventListener('change', handleFileSelect, false);

function handleFileSelect(event) {
  const file = event.target.files[0];
  const reader = new FileReader();

  reader.onload = function(event) {
    const img = new Image();
    img.onload = function() {
      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      canvas.width = img.width;
      canvas.height = img.height;
      ctx.drawImage(img, 0, 0);
      const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
      const pixelData = imageData.data;
      const histogramData = calculateHistogram(pixelData);
      drawHistogram(histogramData);
    };
    img.src = event.target.result;
    document.getElementById('uploadedImage').src = event.target.result;
  };

  reader.readAsDataURL(file);
}

function calculateHistogram(pixelData) {
    const histogram = { R: Array(256).fill(0), G: Array(256).fill(0), B: Array(256).fill(0) };
  
    for (let i = 0; i < pixelData.length; i += 4) {
      const r = pixelData[i];
      const g = pixelData[i + 1];
      const b = pixelData[i + 2];
  
      histogram.R[r]++;
      histogram.G[g]++;
      histogram.B[b]++;
    }
  
    return histogram;
  }
  function drawHistogram(data) {
    const margin = { top: 20, right: 20, bottom: 30, left: 40 };
    const width = 600 - margin.left - margin.right;
    const height = 300 - margin.top - margin.bottom;
  
    const color = d3.scaleOrdinal()
      .domain(["R", "G", "B"])
      .range(["red", "green", "blue"]);
  
    const keys = Object.keys(data);
  
    keys.forEach(key => {
      const values = data[key].filter(value => value !== undefined);
  
      const x = d3.scaleLinear()
        .domain([0, 255])
        .range([0, width]);
  
      const y = d3.scaleLinear()
        .range([height, 0])
        .domain([0, d3.max(values)]);
  
      const xAxis = d3.axisBottom(x);
      const yAxis = d3.axisLeft(y);
  
      const svg = d3.select("#histogram")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);
  
      svg.append("g")
        .attr("class", "axis")
        .attr("transform", `translate(0, ${height})`)
        .call(xAxis);
  
      svg.append("g")
        .attr("class", "axis")
        .call(yAxis);
  
      svg.selectAll(".bar")
        .data(values)
        .enter()
        .append("rect")
        .attr("class", "bar")
        .attr("x", (d, i) => x(i))
        .attr("y", d => y(d))
        .attr("width", width / 256)
        .attr("height", d => height - y(d))
        .style("fill", color(key));
    });
  
    const pixelValues = `Среднее значение R: ${calculateAverage(data['R'])}, Среднее значение G: ${calculateAverage(data['G'])}, Среднее значение B: ${calculateAverage(data['B'])}`;
    document.getElementById('pixelValues').innerText = pixelValues;
  }
  
  
  function calculateAverage(data) {
    const sum = data.reduce((acc, val, idx) => acc + val * idx, 0);
    const totalPixels = data.reduce((acc, val) => acc + val, 0);
    return (sum / totalPixels).toFixed(2);
  }