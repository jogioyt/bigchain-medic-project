var connect = require("../trialCRAB.js");
// create an asset with Alice as owner
connect.bdbOrm.models.myModel
  .create({
    keypair: connect.aliceKeypair,
    data: { key: "dataValue" }
  })
  .then(asset => {
    // lets append update the data of our asset
    // since we use a blockchain, we can only append
    return asset.append({
      toPublicKey: connect.aliceKeypair.publicKey,
      keypair: connect.aliceKeypair,
      data: { key: "updatedValue" }
    });
  })
  .then(updatedAsset => {
    // updatedAsset contains the last (unspent) state
    // of our asset so any actions
    // need to be done to updatedAsset
    console.log(updatedAsset.data);
  });
