var connect = require("../trialCRAB.js");
// from the defined models in our bdbOrm we create an asset with Alice as owner
connect.bdbOrm.models.myModel
  .create({
    keypair: connect.aliceKeypair,
    data: { key: "dataValue" }
  })
  .then(asset => {
    /*
            asset is an object with all our data and functions
            asset.id equals the id of the asset
            asset.data is data of the last (unspent) transaction
            asset.transactionHistory gives the full raw transaction history
            Note: Raw transaction history has different object structure then
            asset. You can find specific data change in metadata property.
        */
    console.log(asset.id);
  });
