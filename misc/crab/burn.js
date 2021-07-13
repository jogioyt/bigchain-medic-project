var connect = require("../trialCRAB.js");
// create an asset with Alice as owner
connect.bdbOrm.models.myModel
  .create({
    keypair: connect.aliceKeypair,
    data: { key: "dataValue" }
  })
  .then(asset => {
    // lets burn the asset by assigning to a random keypair
    // since will not store the private key it's infeasible to redeem the asset
    return asset.burn({ keypair: connect.aliceKeypair });
  })
  .then(burnedAsset => {
    // asset is now tagged as "burned"
    console.log(burnedAsset.data);
  });
