"use strict";
/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
(self["webpackChunkfrontend"] = self["webpackChunkfrontend"] || []).push([["src_components_LastLikesItem_jsx"],{

/***/ "./src/components/LastLikesItem.jsx":
/*!******************************************!*\
  !*** ./src/components/LastLikesItem.jsx ***!
  \******************************************/
/***/ (function(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

eval("__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ \"./node_modules/react/index.js\");\n/* harmony import */ var timeago_react__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! timeago-react */ \"./node_modules/timeago-react/esm/timeago-react.js\");\n\n\n\nvar LastLikesItem = function LastLikesItem(_ref) {\n  var p = _ref.p;\n  return /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement(\"li\", {\n    className: \"list-group-item border-0\"\n  }, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement(\"div\", {\n    className: \"card slide-in-up\"\n  }, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement(\"div\", {\n    className: \"card-body p-2\"\n  }, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement(\"small\", {\n    className: \"card-text text-muted fst-italic d-block mb-1\"\n  }, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement(\"i\", {\n    className: \"fas fa-calendar-check fa-sm me-2\"\n  }), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement(timeago_react__WEBPACK_IMPORTED_MODULE_1__[\"default\"], {\n    datetime: p.timestamp\n  })), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement(\"strong\", null, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement(\"span\", {\n    className: \"badge bg-info rounded-pill\"\n  }, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement(\"a\", {\n    className: \"text-white\",\n    href: \"/profile/\".concat(p.liker)\n  }, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement(\"strong\", {\n    className: \"mb-1\"\n  }, p.liker))), /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement(\"span\", {\n    className: \"text-muted fw-light\"\n  }, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0__.createElement(\"i\", {\n    className: \"fas fa-heartbeat text-danger px-2 py-1 m-0 fa-sm\"\n  })), p.content.split(' ').slice(0, 3).join(' ')))));\n};\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (LastLikesItem);\n\n//# sourceURL=webpack://frontend/./src/components/LastLikesItem.jsx?");

/***/ })

}]);