document.getElementById("calcType").addEventListener("change", function () {
  const showLimit = this.value === "thermalCheck";
  document.getElementById("limitLabel").style.display = showLimit ? "block" : "none";
});

function calculate() {
  const S = parseFloat(document.getElementById("power").value);
  const U = parseFloat(document.getElementById("voltage").value);
  const cosphi = parseFloat(document.getElementById("cosphi").value);
  const type = document.getElementById("calcType").value;
  const limit = parseFloat(document.getElementById("limitCurrent").value);

  const U_V = U * 1000; // в Вольтах
  let resultText = "";

  if (type === "threePhase" || type === "singlePhase") {
    const S_VA = S * 1e6; // МВА → ВА
    const I = S_VA / (Math.sqrt(3) * U_V);
    resultText = `Розрахований струм КЗ: ${I.toFixed(2)} A (${(I / 1000).toFixed(2)} кА)`;
  } else if (type === "thermalCheck") {
    const S_VA = S * 1e6;
    const I = S_VA / (Math.sqrt(3) * U_V);
    const result = I / 1000 <= limit ? "✅ Струм не перевищує граничне значення" : "❌ Струм перевищує допустиме значення";
    resultText = `Розрахований струм КЗ: ${(I / 1000).toFixed(2)} кА. ${result}`;
  }

  document.getElementById("result").textContent = resultText;
}
