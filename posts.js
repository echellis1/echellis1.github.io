// Shared helpers for Featured Posts: content/<yyyymmdd>/index.md
var Posts = (function () {
  var DIR = 'content/';
  var GITHUB_API = 'https://api.github.com/repos/echellis1/ericchellis.github.io/contents/content';

  function text(r) { if (!r.ok) throw new Error(r.status); return r.text(); }

  // Local servers expose a directory listing; GitHub Pages does not, so fall back to the GitHub API.
  function listIds() {
    return fetch(DIR, { cache: 'no-cache' }).then(text).then(function (html) {
      var doc = new DOMParser().parseFromString(html, 'text/html');
      var ids = Array.prototype.map.call(doc.querySelectorAll('a'), function (a) {
        return decodeURIComponent(a.getAttribute('href') || '').replace(/\/$/, '').split('/').pop();
      }).filter(function (n) { return /^\d{8}$/.test(n); });
      if (!ids.length) throw new Error('empty listing');
      return ids;
    }).catch(function () {
      return fetch(GITHUB_API).then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function (items) {
          return items.filter(function (i) { return i.type === 'dir' && /^\d{8}$/.test(i.name); })
                      .map(function (i) { return i.name; });
        });
    }).catch(function () { return []; });
  }

  // Splits "---\nTitle: ...\nDate: ...\nSummary: ...\n---\nbody" into { meta, body }.
  function parse(md) {
    var meta = {}, body = md;
    var m = md.match(/^﻿?---[ \t]*\r?\n([\s\S]*?)\r?\n---[ \t]*(?:\r?\n|$)/);
    if (m) {
      body = md.slice(m[0].length);
      m[1].split(/\r?\n/).forEach(function (line) {
        var kv = line.match(/^([A-Za-z]+):\s*(.*)$/);
        if (kv) meta[kv[1].toLowerCase()] = kv[2].trim();
      });
    }
    return { meta: meta, body: body };
  }

  function load(id) {
    return fetch(DIR + id + '/index.md', { cache: 'no-cache' }).then(text).then(function (md) {
      var p = parse(md);
      p.id = id;
      return p;
    });
  }

  // All posts, newest first by folder name.
  function loadAll() {
    return listIds().then(function (ids) {
      ids.sort().reverse();
      return Promise.all(ids.map(function (id) { return load(id).catch(function () { return null; }); }));
    }).then(function (posts) { return posts.filter(Boolean); });
  }

  // Optional "Image:" front matter (a file in the post's folder); otherwise <yyyymmdd>.jpg.
  function imageSrc(post) {
    return DIR + post.id + '/' + encodeURI(post.meta.image || post.id + '.jpg');
  }

  // An <img> that removes itself if the file doesn't exist.
  function imageEl(post, className) {
    var img = document.createElement('img');
    img.className = className;
    img.src = imageSrc(post);
    img.alt = post.meta.title || post.id;
    img.loading = 'lazy';
    img.onerror = function () { img.remove(); };
    return img;
  }

  // <li><a class="post-card"> with image, title, date and summary.
  function card(post) {
    var li = document.createElement('li');
    var a = document.createElement('a');
    a.className = 'post-card';
    a.href = 'post.html?post=' + post.id;
    a.appendChild(imageEl(post, 'post-card-image'));
    [['post-date', post.meta.date || ''], ['post-title', post.meta.title || post.id], ['post-summary', post.meta.summary || '']]
      .forEach(function (f) {
        if (!f[1]) return;
        var span = document.createElement('span');
        span.className = f[0];
        span.textContent = f[1];
        a.appendChild(span);
      });
    li.appendChild(a);
    return li;
  }

  return { load: load, loadAll: loadAll, imageEl: imageEl, card: card };
})();
