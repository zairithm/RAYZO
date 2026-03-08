use anchor_lang::prelude::*;

declare_id!("FcsZDye6x3AAWheYgvBrz7MKTzx637M4MiVugrykcAcb");

#[program]
pub mod rayzo_auditlayer {
    use super::*;

    pub fn submit_report(
        ctx: Context<SubmitReport>,
        max_probability: f32,
        confidence_score: f32,
        confidence_level: String,
        priority: String,
        triage_score: u8,
        report_hash: String,
    ) -> Result<()> {
  
        let report = &mut ctx.accounts.report;

        report.max_probability = max_probability;
        report.confidence_score = confidence_score;
        report.confidence_level = confidence_level;
        report.priority = priority;
        report.triage_score = triage_score;
        report.report_hash = report_hash;
        report.authority = *ctx.accounts.user.key;

        Ok(())
    }
}

#[derive(Accounts)]
pub struct SubmitReport<'info> {

    #[account(init, payer = user, space = 8 + 200)]
    pub report: Account<'info, ReportAccount>,

    #[account(mut)]
    pub user: Signer<'info>,

    pub system_program: Program<'info, System>,
}

#[account]
pub struct ReportAccount {

    pub max_probability: f32,
    pub confidence_score: f32,
    pub confidence_level: String,
    pub priority: String,
    pub triage_score: u8,
    pub report_hash: String,
    pub authority: Pubkey,
}
