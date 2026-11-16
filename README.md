# Website template

One-page local business website. The design is fixed in `template.html`. `build.py` fills it in from a short `site.json`.

```
python3 build.py site.json site
```

This writes `site/index.html`. Put the photos in `site/img/` first (for example `site/img/p1.jpg`). The script uses only built-in Python, so there's nothing to install.

## site.json fields

See `example-site.json` for a complete example. Only `business_name`, `phone`, `hero_title` and `services` are required. Leave out or empty anything you don't have, and that part of the page disappears.

| Field | What it is |
|---|---|
| `business_name`, `phone` | Required. The phone number can be in any format. |
| `address` | `{street, city, state, zip}`. Used for the location block, the map and the footer. |
| `colors` | `{dark, main, light, accent}` as hex codes: darkest shade, main brand color, very light tint, bright highlight. |
| `logo` | Path to the logo image, like `img/logo.png`, or `""` to use an auto-made icon with the business name. Set `logo_has_name: false` if the logo image doesn't include the name. |
| `rating`, `review_count` | Real Google rating and review count, or leave out. |
| `maps_url` | The business's Google Maps link. |
| `photos` | Every photo path, best first. The first one is the hero background, and the rest are reused to fill other image spots. |
| `hero_image`, `about_image`, `cta_image` | Optional. Choose a specific photo for that spot. |
| `gallery` | Optional. Photos for the gallery. Defaults to all `photos`. |
| `announcement` | Text for the top bar. Leave out to hide the bar. |
| `hero_title` | Wrap one phrase in `*stars*` to color it with the accent color. |
| `hero_subtitle`, `hero_bullets[]` | Hero text and checkmark list. |
| `cta_button`, `form_title`, `form_options[]` | Button text, form heading and dropdown options. The options default to the service titles plus "Other". |
| `services_title`, `services_subtitle`, `services[]` | `{title, text, image}`. 3, 4 or 6 work best. |
| `benefits_eyebrow`, `benefits_title`, `benefits[]` | `{icon (an emoji), title, text}` |
| `about_title`, `about_paragraphs[]`, `stats[]` | `stats` items are `{value, label}`. |
| `reviews[]` | `{name, stars, text}`. Real Google reviews only. |
| `faq[]` | `{q, a}` |
| `hours` | A list of `[day, hours]` pairs or one line of text. |
| `service_area`, `cta_title`, `cta_subtitle`, `page_title`, `meta_description` | Optional text. |

To change the design for every future site, edit `template.html`.
