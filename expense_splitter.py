from flask import Flask, render_template_string, request


app = Flask(__name__)


HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Smart Expense Splitter</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    *{margin:0;padding:0;box-sizing:border-box;font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
    body{
      min-height:100vh;
      padding:24px 10px;
      background:
        radial-gradient(circle at top left,#fde68a 0,#fef9c3 20%,transparent 55%),
        radial-gradient(circle at bottom right,#bfdbfe 0,#e0f2fe 25%,transparent 60%),
        linear-gradient(135deg,#fdfcfb,#e2e8f0);
      color:#111827;
    }
    .container{
      max-width:980px;
      margin:0 auto;
      background:rgba(255,255,255,0.9);
      border-radius:26px;
      padding:22px 18px 26px;
      border:1px solid rgba(209,213,219,0.9);
      box-shadow:
        0 24px 70px rgba(148,163,184,0.45),
        0 0 0 1px rgba(255,255,255,0.9) inset;
      backdrop-filter:blur(18px);
    }
    h1{
      font-size:1.8rem;
      margin-bottom:4px;
      letter-spacing:.03em;
      display:flex;
      align-items:center;
      gap:8px;
    }
    h1::before{
      content:"💸";
      font-size:1.4rem;
    }
    .sub{
      font-size:0.86rem;
      color:#6b7280;
      margin-bottom:16px;
    }
    form{margin-bottom:16px}
    label{
      font-size:0.72rem;
      color:#6b7280;
      display:block;
      margin-bottom:4px;
      text-transform:uppercase;
      letter-spacing:.09em;
    }
    input{
      width:100%;
      padding:9px 10px;
      border-radius:12px;
      border:1px solid #d1d5db;
      background:linear-gradient(135deg,#f9fafb,#ffffff);
      color:#111827;
      font-size:0.9rem;
      margin-bottom:10px;
      transition:border-color .15s,box-shadow .15s,transform .1s;
    }
    input:focus{
      outline:none;
      border-color:#34d399;
      box-shadow:0 0 0 3px rgba(52,211,153,0.25);
      transform:translateY(-1px);
    }
    .friends-row{
      display:grid;
      grid-template-columns:1.4fr 1fr;
      gap:10px;
      margin-bottom:4px;
    }
    .btn{
      margin:12px auto 0;
      width:100%;
      max-width:380px;
      padding:11px 16px;
      border-radius:999px;
      border:none;
      background:linear-gradient(135deg,#22c55e,#14b8a6,#f97316);
      background-size:200% 200%;
      color:#022c22;
      font-weight:600;
      font-size:0.95rem;
      cursor:pointer;
      box-shadow:0 14px 30px rgba(249,115,22,0.35);
      animation:pulse 6s ease-in-out infinite;
      display:block;
    }
    .btn:hover{filter:brightness(1.03)}
    @keyframes pulse{
      0%,100%{background-position:0% 50%}
      50%{background-position:100% 50%}
    }
    .result{
      margin-top:18px;
      padding:16px 14px 12px;
      border-radius:18px;
      background:linear-gradient(135deg,#f9fafb,#eef2ff);
      border:1px solid #e5e7eb;
    }
    .result h2{
      font-size:1.05rem;
      margin-bottom:6px;
      display:flex;
      align-items:center;
      gap:6px;
    }
    .result h2::before{content:"📊"}
    .pill{
      font-size:0.8rem;
      color:#6b7280;
      margin-bottom:8px;
      padding:7px 9px;
      border-radius:999px;
      background:rgba(219,234,254,0.8);
      border:1px dashed #bfdbfe;
    }
    .grid{
      display:grid;
      grid-template-columns:repeat(auto-fit,minmax(230px,1fr));
      gap:10px;
      margin-top:8px;
    }
    .card{
      background:radial-gradient(circle at top left,#eff6ff,transparent 55%),#ffffff;
      border-radius:14px;
      border:1px solid #e5e7eb;
      padding:10px 11px 9px;
      font-size:0.82rem;
      box-shadow:0 10px 24px rgba(148,163,184,0.35);
    }
    .card-header{
      display:flex;
      justify-content:space-between;
      margin-bottom:6px;
      align-items:center;
    }
    .name{font-weight:600;color:#111827}
    .amount{font-weight:700;color:#16a34a}
    .meta{
      font-size:0.72rem;
      color:#6b7280;
      margin-top:3px;
      line-height:1.4;
    }
    .small{font-size:0.72rem;color:#9ca3af;margin-top:2px}
    .error{
      margin-top:10px;
      color:#b91c1c;
      font-size:0.8rem;
      background:#fee2e2;
      border-radius:10px;
      padding:8px 10px;
      border:1px solid #fecaca;
    }
    .inline{
      display:flex;
      gap:8px;
      flex-wrap:wrap;
      font-size:0.78rem;
      margin-bottom:10px;
      color:#4b5563;
      background:rgba(240,249,255,0.9);
      border-radius:12px;
      padding:8px 10px;
      border:1px dashed #93c5fd;
    }
    .inline span strong{color:#111827}
    .totals{font-size:0.8rem;color:#6b7280;margin-top:8px}
    .totals strong{color:#111827}

    /* Mobile tweaks */
    @media(max-width:640px){
      body{padding:18px 8px;}
      .container{padding:18px 14px 22px;border-radius:20px;}
      h1{font-size:1.5rem;}
      .friends-row{grid-template-columns:1fr;}
      .btn{font-size:0.9rem;padding:10px 14px;}
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>Smart Expense Splitter</h1>
    <p class="sub">
      Each friend orders different items. Enter their original amounts and the final bill after offer.
      The app splits the final total fairly and also shows a rounded value for easy payment.
    </p>

    <form method="POST">
      <label>Number of friends</label>
      <input type="number" name="count" min="1" max="10" value="{{ count or '' }}" placeholder="e.g. 3" required>

      <label>Final bill amount (after Instamart / JioMart offer)</label>
      <input type="number" step="0.01" name="final_total" value="{{ final_total or '' }}" placeholder="e.g. 420" required>

      <div class="inline">
        <span>💡 Everyone's share is proportional to their original order.</span>
      </div>

      {% if count %}
        {% for i in range(count) %}
        <div class="friends-row">
          <div>
            <label>Friend {{ i+1 }} name</label>
            <input type="text" name="name_{{ i }}" placeholder="Friend {{ i+1 }}">
          </div>
          <div>
            <label>Original amount (their cart value)</label>
            <input type="number" step="0.01" name="amount_{{ i }}" placeholder="0.00">
          </div>
        </div>
        {% endfor %}
      {% endif %}

      <button class="btn" type="submit">Split Fairly ✨</button>
    </form>

    {% if error %}
      <div class="error">{{ error }}</div>
    {% endif %}

    {% if shares %}
    <div class="result">
      <h2>Split summary</h2>
      <div class="pill">
        Total original: ₹{{ total_original }} · Final bill: ₹{{ final_total }}.
        Each card shows <strong>exact</strong> share and a <strong>rounded</strong> amount to pay.
      </div>
      <div class="grid">
        {% for s in shares %}
        <div class="card">
          <div class="card-header">
            <span class="name">{{ s.name }}</span>
            <span class="amount">Pay (rounded): ₹{{ "%.0f"|format(s.rounded_share) }}</span>
          </div>
          <div class="meta">
            Ordered: ₹{{ "%.2f"|format(s.original) }}<br>
            Exact fair share: ₹{{ "%.2f"|format(s.exact_share) }}<br>
            Discount vs original: ₹{{ "%.2f"|format(s.discount) }} ({{ "%.1f"|format(s.discount_percent) }}% off)
          </div>
          <div class="small">
            Rounded difference from exact: {{ "+" if s.rounded_share - s.exact_share >= 0 else "" }}₹{{ "%.2f"|format(s.rounded_share - s.exact_share) }}
          </div>
        </div>
        {% endfor %}
      </div>
      
    </div>
    {% endif %}
  </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    count = None
    final_total = ""
    shares = []
    error = None
    total_original = 0.0
    rounded_sum = 0.0

    if request.method == "POST":
        try:
            raw_count = request.form.get("count", "").strip()
            if not raw_count:
                raise ValueError("No count")
            count = int(raw_count)
            count = max(1, min(count, 10))  # 1–10 friends

            final_total = request.form.get("final_total", "").strip()
            final_total_val = float(final_total)

            names, amounts = [], []
            for i in range(count):
                name = request.form.get(f"name_{i}", "").strip() or f"Friend {i+1}"
                amt_str = request.form.get(f"amount_{i}", "").strip() or "0"
                amt = float(amt_str)
                names.append(name)
                amounts.append(amt)

            total_original = sum(amounts)

            if total_original <= 0:
                error = "Total original amount must be greater than 0."
            else:
                # exact proportional shares (standard fair split) [web:156][web:161]
                exact_shares = [final_total_val * (a / total_original) for a in amounts]

                # round to nearest rupee
                rounded = [round(x) for x in exact_shares]

                # adjust so sum(rounded) == final_total
                rounded_sum = sum(rounded)
                diff = int(round(final_total_val - rounded_sum))
                idx = 0
                step = 1 if diff > 0 else -1
                while diff != 0 and rounded:
                    rounded[idx] += step
                    diff -= step
                    idx = (idx + 1) % len(rounded)
                rounded_sum = sum(rounded)

                for name, original, exact, rnd in zip(names, amounts, exact_shares, rounded):
                    discount = original - exact
                    discount_percent = (discount / original * 100) if original > 0 else 0.0
                    shares.append(
                        type("Share", (), {
                            "name": name,
                            "original": original,
                            "exact_share": exact,
                            "rounded_share": rnd,
                            "discount": discount,
                            "discount_percent": discount_percent
                        })
                    )

        except ValueError:
            error = "Please enter valid numbers for count, amounts, and final total."

    return render_template_string(
        HTML,
        count=count,
        final_total=final_total,
        shares=shares,
        total_original=f"{total_original:.2f}",
        rounded_sum=f"{rounded_sum:.0f}",
        error=error,
    )


if __name__ == "__main__":
    print("🚀 Smart Expense Splitter running on http://127.0.0.1:5000")
    app.run(debug=True)


