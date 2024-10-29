module.exports = {
    apps : [{
      name: 'temp-varsel',
      script: 'python3',
      args: 'Temperatur_varsel.py',
      instances: 1,
      autorestart: true,
      watch: false
    }, {
      name: 'oppdateringer',
      script: 'python3',
      args: 'Sjekk_for_oppdateringer.py',
      instances: 1,
      autorestart: true,
      watch: false
    }],
  };