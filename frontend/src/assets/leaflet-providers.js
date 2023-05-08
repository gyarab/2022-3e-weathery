(function (root, factory) {
    let define;
    let modules
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module.
        define(['leaflet'], factory);
    } else if (typeof modules === 'object' && module.exports) {
        // define a Common JS module that relies on 'leaflet'
        module.exports = factory(require('leaflet'));
    } else {
        // Assume Leaflet is loaded into global object L already
        factory(L);
    }
}(this, function (L) {
    'use strict';

    L.TileLayer.Provider = L.TileLayer.extend({
        initialize: function (arg, options) {
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

            // overwrite values in provider from variant.
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
                return attr.replace(/\{attribution.(\w*)/g,
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

    /**
     * Definition of providers.
     * see http://leafletjs.com/reference.html#tilelayer for options in the options map.
     */

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
                Positron: 'light_all',
                Voyager: 'rastertiles/voyager',
            }
        },
    };

    L.tileLayer.provider = function (provider, options) {
        return new L.TileLayer.Provider(provider, options);
    };

    return L;
}));
