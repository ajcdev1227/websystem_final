(function () {
  "use strict";

  const module = { exports: window }

  const jsonMimeRegex = /^(?:application|text)\/json(?:;.*)?$/;

  class ApiResponseError extends Error {
    /**
     * @type {Response}
     */
    response

    /**
     * @type {string}
     */
    body

    /**
     *
     * @param {string} message
     * @param {Response} response
     * @param {string} body
     */
    constructor(message, response, body) {
      super(message)
      this.response = response
      this.body = body
    }
  }

  class ApiStatusError extends ApiResponseError {
    /**
     * @type {number}
     */
    status

    /**
     * @type {string}
     */
    apiMessage

    /**
     *
     * @param {string} message
     * @param {Response} response
     * @param {string} body
     * @param {string | undefined} apiMessage
     */
    constructor(message, response, body, status, apiMessage) {
      super(message, response, body)

      this.status = status
      this.apiMessage = apiMessage
    }
  }

  /**
   * Makes an API request and returns the JSON response, or throws an error if something went wrong
   * @param {'GET'|'POST'|'PUT'|'DELETE'} method The request method
   * @param {string} path The request path or URL
   * @param {Record<string, any>} [query] Any query parameters to include (optional)
   * @param {Record<string, any>} [body] The request body JSON data to send (optional, has no effect on GET and DELETE)
   * @returns {Promise<T>} The response
   * @template T
   */
  async function apiReq(method, path, query, body) {
    const queryStr = new URLSearchParams(query ?? {}).toString()

    /** @type {HeadersInit} */
    const headers = {}

    /** @type {RequestInit} */
    const ops = {
      method,
      headers,
      credentials: 'same-origin',
      redirect: 'follow',
    }

    if (method !== 'GET' && method !== 'DELETE' && body != null) {
      headers['Content-Type'] = 'application/json'
      ops.body = JSON.stringify(body)
    }

    const res = await fetch(queryStr === '' ? path : path + '?' + queryStr, ops)

    const contentType = res.headers.get('Content-Type')?.toLowerCase() ?? ''

    if (!jsonMimeRegex.test(contentType)) {
      throw new ApiResponseError(`The ${method} request to ${path} returned a non-JSON response`, res, await res.text())
    }

    if (res.status < 200 || res.status > 299) {
      const body = await res.text()

      /** @type {string | undefined} */
      let apiMessage = undefined

      try {
        apiMessage = JSON.parse(body).message
      } catch (_) {}

      throw new ApiStatusError(`The ${method} request to ${path} returned non-2XX response`, res, body, res.status, apiMessage)
    }

    return await res.json()
  }

  /**
   * Makes an API GET request
   * @param {string} path The path
   * @param {Record<string, any>} [query] The query parameters to pass (optional)
   * @returns {Promise<T>}
   * @template T
   */
  function apiGet(path, query) {
    return apiReq('GET', path, query)
  }

  /**
   * Makes an API POST request
   * @param {string} path The path
   * @param {Record<string, any>} [query] The query parameters to pass (optional)
   * @param {Record<string, any>} [body] The request body (optional)
   * @returns {Promise<T>}
   * @template T
   */
  function apiPost(path, query, body) {
    return apiReq('POST', path, query, body)
  }

  /**
   * Makes an API PUT request
   * @param {string} path The path
   * @param {Record<string, any>} [query] The query parameters to pass (optional)
   * @param {Record<string, any>} [body] The request body (optional)
   * @returns {Promise<T>}
   * @template T
   */
  function apiPut(path, query, body) {
    return apiReq('PUT', path, query, body)
  }

  /**
   * Makes an API DELETE request
   * @param {string} path The path
   * @param {Record<string, any>} [query] The query parameters to pass (optional)
   * @returns {Promise<T>}
   * @template T
   */
  function apiDelete(path, query) {
    return apiReq('DELETE', path, query)
  }

  module.exports.apiReq = apiReq
  module.exports.apiGet = apiGet
  module.exports.apiPost = apiPost
  module.exports.apiPut = apiPut
  module.exports.apiDelete = apiDelete

  // show and hide sidebar

  const body = document.querySelector("body");
  const sidebarShowBtn = document.querySelector(".sidebar-header .sidebar-btn");
  const sidebar = document.querySelector(".sidebar-wrapper");
  const bodyGrid = document.querySelector(".body-grid");

  bodyGrid.style.gridTemplateColumns = `${sidebar.offsetWidth}px 1fr`;

  sidebarShowBtn.addEventListener("click", () => {
    sidebar.classList.toggle("active");
    sidebarShowBtn.classList.toggle("active");
    const icon = sidebarShowBtn.querySelector("i");
    if (sidebarShowBtn.classList.contains("active")) {
      icon.className = "bx bxs-chevrons-left";
      body.style.overflow = "hidden";

      // get sidebar width dynamically

      sidebarShowBtn.style.left = `calc(${sidebar.offsetWidth}px - 5px)`;
    } else {
      icon.className = "bx bxs-chevrons-right";
      sidebarShowBtn.style.left = "5px";
      body.style.overflow = "auto";
    }
  });

  // sidebar links add and remove active class

  const sidebarLinks = document.querySelectorAll(".sidebar ul li a");

  sidebarLinks.forEach((links) => {
    links.addEventListener("click", function () {
      sidebarLinks.forEach((link) => link.classList.remove("active"));
      this.classList.add("active");
    });
  });


})()
