/*
 * Copyright 2016 Google Inc. All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
'use strict';

// Create viewer.
var viewer = new Marzipano.Viewer(document.getElementById('pano'));

// The tiles were generated with the krpano tools, which index the tiles
// from 1 instead of 0. Hence, we cannot use ImageUrlSource.fromString()
// and must write a custom function to convert tiles into URLs.
var urlPrefix = "tiles";
var tileUrl = function(z, x, y) {
  return urlPrefix + "/z" + z + "/x" + x +  "/" + z + '-' + x + '-' + y + ".jpg";
};
var source = new Marzipano.ImageUrlSource(function(tile) {
  return { url: tileUrl(tile.z, tile.x, tile.y) };
});
