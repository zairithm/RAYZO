import * as anchor from "@coral-xyz/anchor";
import { Program } from "@coral-xyz/anchor";
import { RayzoAuditlayer } from "../target/types/rayzo_auditlayer";

describe("rayzo_auditlayer", () => {

  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);

  const program = anchor.workspace.RayzoAuditlayer as Program<RayzoAuditlayer>;

  it("Submit report", async () => {

    const reportAccount = anchor.web3.Keypair.generate();

    await program.methods
      .submitReport(
        0.001,
        0.001,
        "Low",
        "LOW",
        0,
        "hash123"
      )
      .accounts({
        report: reportAccount.publicKey,
        user: provider.wallet.publicKey,
        systemProgram: anchor.web3.SystemProgram.programId,
      } as any)   // <-- ye TypeScript error fix karta hai
      .signers([reportAccount])
      .rpc();

    console.log("Report submitted:", reportAccount.publicKey.toString());

  });

});