// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-home",
    title: "Home",
    section: "Navigation",
    handler: () => {
      window.location.href = "/photo/";
    },
  },{id: "nav-collection",
          title: "Collection",
          description: "Browse the complete collection of Jason&#39;s Ancient Coins",
          section: "Navigation",
          handler: () => {
            window.location.href = "/photo/collection/";
          },
        },{id: "coins-p-porcius-laeca-provocatio",
          title: 'P. Porcius Laeca - Provocatio',
          description: "",
          section: "Coins",handler: () => {
              window.location.href = "/photo/coins/p_porcius_laeca/";
            },},{id: "coins-denarius-of-p-licinius-nerva",
          title: 'Denarius of P. Licinius Nerva',
          description: "",
          section: "Coins",handler: () => {
              window.location.href = "/photo/coins/p_licinius_nerva/";
            },},{id: "coins-gaius-pansa-and-decimus-brutus-48-bce-rome",
          title: 'Gaius Pansa and Decimus Brutus – 48 BCE – Rome',
          description: "",
          section: "Coins",handler: () => {
              window.location.href = "/photo/coins/pansa_brutus/";
            },},{id: "coins-denarius-of-faustus-cornelius-sulla",
          title: 'Denarius of Faustus Cornelius Sulla',
          description: "",
          section: "Coins",handler: () => {
              window.location.href = "/photo/coins/faustus_sulla/";
            },},{id: "coins-denarius-of-julius-caesar",
          title: 'Denarius of Julius Caesar',
          description: "",
          section: "Coins",handler: () => {
              window.location.href = "/photo/coins/julius_caesar/";
            },},{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];
