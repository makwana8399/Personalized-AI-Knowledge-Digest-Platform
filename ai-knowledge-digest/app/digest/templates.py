from datetime import date
import html


class Templates:
    @staticmethod
    def get_email_template(overview: str, articles: list[dict]) -> str:
        today = date.today().strftime("%B %d, %Y")

        def safe(text: str) -> str:
            """Escape + clean AI output for email"""
            if not text:
                return ""
            text = text.replace("```", "").strip()
            return html.escape(text)

        articles_html = ""

        for article in articles:
            title = safe(article.get("title", "Untitled"))
            summary = safe(article.get("summary", ""))
            url = article.get("url", "#")
            source = article.get("source", "").lower()

            # Badge
            badge = ""
            if source == "youtube":
                badge = """
                <span style="background:#ff0000;color:#fff;
                             padding:3px 8px;border-radius:12px;
                             font-size:11px;margin-left:6px;">
                  YouTube
                </span>
                """
            elif source == "newsletter":
                badge = """
                <span style="background:#34a853;color:#fff;
                             padding:3px 8px;border-radius:12px;
                             font-size:11px;margin-left:6px;">
                  Newsletter
                </span>
                """

            articles_html += f"""
            <tr>
              <td style="padding-top:25px;">
                <h3 style="margin:0;font-size:18px;color:#111;">
                  {title}{badge}
                </h3>
              </td>
            </tr>

            <tr>
              <td style="padding-top:8px;
                         font-size:14px;
                         color:#333;
                         line-height:1.6;">
                {summary}
              </td>
            </tr>

            <tr>
              <td style="padding-top:10px;">
                <a href="{url}"
                   style="color:#1a73e8;
                          text-decoration:none;
                          font-size:14px;">
                  Read full article →
                </a>
              </td>
            </tr>

            <tr>
              <td style="padding-top:20px;
                         border-bottom:1px solid #e0e0e0;">
              </td>
            </tr>
            """

        return f"""
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Daily AI News Digest</title>
</head>

<body style="margin:0;
             padding:0;
             background-color:#f6f6f6;
             font-family:Arial,Helvetica,sans-serif;">

<table width="100%" cellpadding="0" cellspacing="0">
  <tr>
    <td align="center">

      <table width="600" cellpadding="0" cellspacing="0"
             style="background:#ffffff;
                    padding:24px;
                    margin-top:20px;">

        <!-- Header -->
        <tr>
          <td>
            <h2 style="margin:0;
                       font-size:22px;
                       color:#111;">
              🧠 Daily AI News Digest
            </h2>
            <p style="margin:6px 0 0;
                      font-size:13px;
                      color:#777;">
              {today}
            </p>
          </td>
        </tr>

        <tr>
          <td style="padding-top:15px;
                     border-bottom:2px solid #000;">
          </td>
        </tr>

        <!-- Intro -->
        <tr>
          <td style="padding-top:20px;
                     font-size:14px;
                     color:#333;">
            Hello 👋 — here’s your personalized AI & tech update.
          </td>
        </tr>

        <!-- Overview -->
        <tr>
          <td style="padding-top:14px;
                     font-size:14px;
                     color:#333;
                     line-height:1.6;">
            {safe(overview)}
          </td>
        </tr>

        <!-- Articles -->
        {articles_html}

        <!-- Footer -->
        <tr>
          <td style="padding-top:30px;
                     font-size:12px;
                     color:#777;
                     text-align:center;">
            You’re receiving this because you subscribed to the AI Knowledge Digest.<br>
            Built with ❤️ using AI.
          </td>
        </tr>

      </table>

    </td>
  </tr>
</table>

</body>
</html>
"""