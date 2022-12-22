(function(root, factory) {
  if (typeof define === 'function' && define.amd) {
    define(['leaflet'], factory);
  } else if (typeof module === 'object' && module.exports) {
    module.exports = factory(require('leaflet'));
  } else {
    factory(L);
  }
}(this, function(L) {
  'use strict';

  L.TileLayer.Provider = L.TileLayer.extend({
    initialize: function(arg, options) {
      let providers = L.TileLayer.Provider.providers;
      let parts = arg.split('.');
      let providerName = parts[0];
      let variantName = parts[1];
      if (!providers[providerName]) {
        throw 'No such provider (' + providerName + ')';
      }
      let provider = {
        url: providers[providerName].url,
        options: providers[providerName].options
      };
      if (variantName && 'variants' in providers[providerName]) {
        if (!(variantName in providers[providerName].variants)) {
          throw 'No such variant of ' + providerName + ' (' + variantName + ')';
        }
        let variant = providers[providerName].variants[variantName];
        let variantOptions;
        if (typeof variant === 'string') {
          variantOptions = {
            variant: variant
          };
        } else {
          variantOptions = variant.options;
        }
        provider = {
          url: variant.url || provider.url,
          options: L.Util.extend({}, provider.options, variantOptions)
        };
      }

      let attributionReplacer = function (attr) {
        if (attr.indexOf('{attribution.') === -1) {
          return attr;
        }
        return attr.replace(/\{attribution.(\w*)\}/g,
            function (match, attributionName) {
              return attributionReplacer(providers[attributionName].options.attribution);
            }
        );
      };
      provider.options.attribution = attributionReplacer(provider.options.attribution);
      let layerOpts = L.Util.extend({}, provider.options, options);
      L.TileLayer.prototype.initialize.call(this, provider.url, layerOpts);
    }
  });
  L.TileLayer.Provider.providers = {
    OpenStreetMap: {
      url: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
      options: {
        maxZoom: 19,
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      },
    },
    CartoDB: {
      url: 'https://{s}.basemaps.cartocdn.com/{variant}/{z}/{x}/{y}{r}.png',
      options: {
        attribution: '{attribution.OpenStreetMap} &copy; <a href="https://carto.com/attributions">CARTO</a>',
        subdomains: 'abcd',
        maxZoom: 20,
        variant: 'light_all'
      },
      variants: {
        Voyager: 'rastertiles/voyager',
      }
    },
  };
  L.tileLayer.provider = function(provider, options) {
    return new L.TileLayer.Provider(provider, options);
  };
  return L;
}));
